import logging
from typing import Dict, Any, NoReturn

from magmalt.core import ContextAwareMixin
from .models import Models
logger = logging.getLogger('model_builder')


class ModelBuilder:
    def __init__(self, context):
        self.context = context

    def create_model(self, model_name, model_config):
        logger.debug("Create model %s", model_name)
        instance_cls = Models[model_config.pop('instance')]
        try:
            model = instance_cls(name=model_name,
                                 context=self.context,
                                 **model_config)

        except Exception as err:
            logging.error("During creation of model %s got error: %s",
                          model_name, str(err))
            raise err
        return model

    def build(self, models_config: Dict[str, Dict]) -> NoReturn:
        for model_name, model_config in models_config.items():
            self.context.models[model_name] = self.create_model(
                model_name=model_name, model_config=model_config)
