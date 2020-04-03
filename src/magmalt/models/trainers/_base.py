import logging
from magmalt.core import Step

logger = logging.getLogger('trainer')


class Trainer(Step):
    def __init__(self, name, context, dataset: str, model: str, **kwargs):
        super().__init__(name=name, context=context, **kwargs)
        try:
            self.model = self.context.models[model]
        except KeyError as err:
            logger.error(
                "%s: cannot find model '%s' in context. Available models: %s",
                name, model, " ".join(self.context.models.keys()))
        self.dataset = dataset
        self.options = kwargs

    def train(self):
        pass

    def initialize(self):
        logger.debug('%s create model %s', self.name, self.model.name)

        self.model.initialize()
        return True