import logging
from typing import Type, Dict, Any

from magmalt.core import Factory
from magmalt.instances import Instances

logger = logging.getLogger('steps_factory')


class StepsFactory(Factory):
    def __init__(self, context):
        super().__init__(context=context, config_section='steps')

    def get_instance(self, step_name: str, step_config: Dict[str,
                                                             Any]) -> Type:

        instance = step_config.pop('instance', None)
        logger.debug('Finding isntance %s for step %s', instance, step_name)
        if instance is None:
            raise ValueError(
                f"Field 'instance' is not set for step {step_name}")
        instance_cls = Instances.get(instance, None)
        if instance_cls is None:
            raise ValueError(
                f"'{instance}' instance is not defined in Instances for step "
                f"{step_name}")

        return instance_cls


# class StepsBuilder(ContextAwareMixin):
#     def create_step(self, step_name, step_config):
#         logger.debug("Create step %s", step_name)
#         instance = step_config.pop('instance', None)
#         if instance is None:
#             raise ValueError(
#                 f"Field 'instance' is not set for step {step_name}")
#         instance_cls = Instances.get(instance, None)
#         if instance_cls is None:
#             raise ValueError(
#                 f"'{instance}' instance is not defined in "
#                  "Instances for step "
#                 f"{step_name}")
#         return instance_cls(name=step_name,
#                             context=self.context,
#                             **step_config)

#     def build(self, steps_config):
#         steps = []
#         for step_name, step_config in steps_config.items():
#             steps.append(
#                 self.create_step(step_name=step_name,
#                                   step_config=step_config))
#         return steps
