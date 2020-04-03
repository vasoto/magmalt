import logging
from typing import Dict, Any, Optional, Callable

from ._base import Trainer

logger = logging.getLogger('xgboost_trainer')


class XGBoostModelTrainer(Trainer):
    # def __init__(self, name: str, context, model: str, dataset: str, **kwargs):
    #     super().__init__(name=name,
    #                      context=context,
    #                      model=model,
    #                      dataset=dataset)

    def train(self):
        pass

    def initialize(self):
        return True