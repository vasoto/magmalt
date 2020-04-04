import logging

from typing import Dict, Any, NoReturn
from magmalt.core import Dataset

logger = logging.getLogger('dataset_builder')


class DatasetBuilder:
    def __init__(self, context):
        self.context = context

    def build(self, configuration: Dict[str, Any]) -> NoReturn:
        dataset_conf = configuration.get(
            'datasets', {})  # Do not pop - will be needed for reader
        for name, config in dataset_conf.items():
            logger.debug("Configure dataset %s", name)
            self.context.datasets[name] = Dataset(name=name, **config)
