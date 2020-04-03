import logging
from typing import Dict, Any, Type, Union


class Factory:
    def __init__(self, context, config_section):
        self.context = context
        self.config_section = config_section
        self.steps = []

    def get_instance(self, name: str, config: Dict[str, Any]) -> Type:
        raise NotImplementedError("Method 'get_instance' is not defined")

    def create_step(self, name: str, step_config: Union[Dict[str, Any],
                                                        None]) -> Any:
        if step_config is None:
            step_config = {}
        instance_class = self.get_instance(name, step_config)
        try:
            step = instance_class(name=name,
                                  context=self.context,
                                  **step_config)
        except Exception as err:
            # Log error for clarity
            if instance_class is None:
                logging.error(
                    'Step instance is None. Check get_instance method.')
            else:
                logging.error("Error creating instance of %s (%s): %s",
                              instance_class.__name__, name, err)
            raise err
        return step

    def create_all(self, configuration: Dict[str, Any]):
        self.steps = [
            self.create_step(step_name, step_config) for step_name, step_config
            in configuration[self.config_section].items()
        ]
        return self