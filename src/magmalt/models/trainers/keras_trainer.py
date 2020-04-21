import logging
from typing import Dict, Any, Optional, Callable, List

# Support Tensorflow built-in Keras
from tensorflow import keras
from tensorflow.keras import optimizers
from tensorflow.keras import callbacks as keras_callbacks

from ._base import Trainer
from magmalt.core import Factory

logger = logging.getLogger('keras_trainer')


def create_callback(cback_name, params):
    instance_class_name = params.pop('instance', None)
    if instance_class_name is None:
        ValueError('Class instance is not set for '
                   'Keras callback %s', cback_name)
    instance_class = getattr(keras_callbacks, instance_class_name, None)
    if instance_class is None:
        raise ValueError('%s is not a valid Keras callback (%s)',
                         instance_class_name, cback_name)
    return instance_class(**params)


class KerasModelTrainer(Trainer):
    def __init__(self,
                 name: str,
                 context,
                 model: str,
                 dataset: str,
                 optimizer: Dict[str, Any] = {'instance': 'Adam'},
                 loss: str = 'mse',
                 metrics: List[str] = ['mse', 'mae'],
                 eval_metric: str = 'rmse',
                 test_split_ratio: float = 0.2,
                 epochs=100,
                 batch_size=1024,
                 callbacks: Optional[Dict[str, Any]] = {}):
        super().__init__(name=name,
                         context=context,
                         dataset=dataset,
                         model=model)

        self.optimizer = KerasModelTrainer.get_optimizer(**optimizer)
        self.dataset = dataset
        self.test_split_ratio = test_split_ratio
        self.batch_size = batch_size
        self.callbacks_params = callbacks
        self.callbacks = []
        self.epochs = epochs
        self.loss = loss
        self.metrics = metrics

    @staticmethod
    def get_optimizer(instance, **optimizer_params):
        optimizer_cls = getattr(optimizers, instance)
        return optimizer_cls(**optimizer_params)

    def initialize(self):
        result = super().initialize()
        if result:
            logger.debug("Compiling Keras model %s", self.model.name)
            self.model.model.compile(optimizer=self.optimizer,
                                     loss=self.loss,
                                     metrics=self.metrics)
            self.model.model.summary()
            self._create_callbacks()

        return result

    def _get_train_data(self):
        data = self.context.datasets[self.dataset].data
        X = data[self.model.inputs].values
        y = data[self.model.outputs].values
        return X, y

    def _create_callbacks(self):
        for callback_name, options in self.callbacks_params.items():
            self.callbacks.append(create_callback(callback_name, options))

    def _train_model(self, X, y):
        # Get built model from context

        self.model.model.fit(X,
                             y,
                             callbacks=self.callbacks,
                             epochs=self.epochs,
                             batch_size=self.batch_size,
                             validation_split=self.test_split_ratio,
                             use_multiprocessing=False)

    def run(self):
        # fit model
        logger.debug('Running training for model %s', self.model.name)
        X, y = self._get_train_data()
        self._train_model(X, y)
        return True
