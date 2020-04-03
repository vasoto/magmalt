import logging
from typing import Dict, Any, Optional, Callable
try:
    from tensorflow import keras
    from tensorflow.keras import optimizers
except Exception as _:
    import keras
    from keras import optimizers
    logging.warning('Upgrade Tensorflow!')

from ._base import Trainer

logger = logging.getLogger('keras_trainer')


class KerasModelTrainer(Trainer):
    def __init__(self,
                 name: str,
                 context,
                 model: str,
                 dataset: str,
                 optimizer: Dict[str, Any] = {'instance': 'Adam'},
                 eval_metric: str = 'rmse',
                 test_split_ratio: float = 0.2,
                 callbacks: Optional[Dict[str, Callable]] = {}):
        super().__init__(name=name,
                         context=context,
                         dataset=dataset,
                         model=model)

        self.optimizer = KerasModelTrainer.get_optimizer(**optimizer)
        self.dataset = dataset
        self.test_split_ratio = test_split_ratio
        self.callbacks = callbacks

    @staticmethod
    def get_optimizer(instance, **optimizer_params):
        optimizer_cls = getattr(optimizers, instance)
        return optimizer_cls(**optimizer_params)

    def run(self):
        return True