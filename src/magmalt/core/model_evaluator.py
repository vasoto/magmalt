import logging

from .step import Step
from .model import Model

logger = logging.getLogger('model_evaluator')


class ModelEvaluator(Step):
    def __init__(self, name: str, context, model: str, dataset: str,
                 results: str, **kwargs):
        super().__init__(context=context, name=name)
        self.model = model
        self.dataset = dataset
        self.results = results

    def initialize(self):
        """
        """
        # add evaluated model's features to evaluation dataset
        model: Model = self.context.models[self.model]
        logger.debug(
            "Append model %s inputs and outputs to dataset %s features'",
            self.model, self.dataset)
        dataset = self.context.datasets[self.dataset]
        model.update_dataset_features(dataset=dataset)
        return True

    def evaluate(self):
        self.context.datasets[self.results] = self.context.datasets[
            self.dataset]

    def run(self):
        self.evaluate()
        return True