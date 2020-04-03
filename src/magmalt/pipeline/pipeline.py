from collections import OrderedDict
import logging

from magmalt.core import ContextAwareMixin, Context
from magmalt.models.model_builder import ModelBuilder
# from .step import Step
from .step_factory import StepsFactory
from magmalt.data.builder import DatasetBuilder
from magmalt.metrics.metrics_factory import MetricsFactory
from magmalt.data.reader_factory import ReaderFactory
logger = logging.getLogger('pipeline')


class Pipeline(ContextAwareMixin):
    """ Main pipeline manager
    """
    def __init__(self, context, name=''):
        super().__init__(context=context, name=name)
        self.context.owner = self
        self.steps: Dict[str, "Step"] = dict()

    @classmethod
    def _create_steps(cls, config, context):
        steps = [
            Step.create(name=step_name, context=context, config=step_config)
            for step_name, step_config in config.pop('steps', {}).items()
        ]
        return steps

    @staticmethod
    def _create_steps(config, context):
        steps = OrderedDict()
        factories = [ReaderFactory, StepsFactory]
        for factory_cls in factories:
            factory = factory_cls(context=context).create_all(config)
            for step in factory.steps:
                if step.name in steps:
                    logger.warning(
                        "Step named %s is already present in the pipeline. The previous step will be overwritten."
                    )
                steps[step.name] = step
        return steps

    @staticmethod
    def _add_metrics(context, config):
        # Populate metrics section of context
        context.metrics = {
            metric.name: metric
            for metric in MetricsFactory(context).create_all(config).steps
        }

    @classmethod
    def create(cls, config, context=Context()):
        name = config.pop('name', '')
        pipeline = Pipeline(name=name, context=context)
        DatasetBuilder(context).build(config)
        ModelBuilder(context).build(config.pop('models', {}))
        cls._add_metrics(context=context, config=config)
        pipeline.steps = cls._create_steps(context=context, config=config)
        return pipeline

    def apply_step_method(self, method_name: str, raise_unavailable=False):
        for step in self.steps.values():
            # Assume all steps contain the mentioned method,
            # otherwise AttributeError is raised
            method = getattr(step, method_name, None)
            logger.debug("Run method %s for step %s", method_name, step.name)
            try:
                result = method()
            except Exception as err:
                result = False
                logger.error("Error while running %s for step %s: %s",
                             method_name, step.name, str(err))
            if not result:
                logger.warning(
                    "%s method did not succeed for step %s. Stopping pipeline.",
                    method_name, step.name)
                return False
        return True

    def initialize(self):
        return self.apply_step_method('initialize')

    def run(self):
        return self.apply_step_method('run')

    def __enter__(self):
        logger.debug("Initialize pipeline from context manager")
        if not self.initialize():
            raise ValueError("Cannot initialize pipeline")
        return self

    def __exit__(self, type, value, traceback):
        logger.debug("Exit pipeline context manager")
