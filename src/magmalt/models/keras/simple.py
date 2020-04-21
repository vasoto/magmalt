import logging

from tensorflow import keras

from magmalt.core import Model

logger = logging.getLogger('keras_simple_model')


class KerasSimpleModel(Model):
    def __init__(self,
                 name,
                 context,
                 inputs,
                 outputs,
                 layers,
                 dataset,
                 hidden_activation='relu',
                 output_activation='sigmoid',
                 use_batch_normalization=True,
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 dropout_rate=0.0):
        super().__init__(name=name,
                         context=context,
                         inputs=inputs,
                         outputs=outputs,
                         dataset=dataset)
        self.layers = layers
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer
        self.hidden_activation = hidden_activation
        self.output_activation = output_activation
        self.use_batch_normalization = use_batch_normalization
        self.dropout_rate = dropout_rate

    def create(self):
        """ Create the model
        """
        input_dim = len(self.inputs)
        output_dim = len(self.outputs)
        # Simple, sequential model
        model = keras.Sequential()
        # Create input layer
        model.add(keras.layers.Input(shape=(input_dim, ), name='Inputs'))
        if self.use_batch_normalization:
            model.add(
                keras.layers.BatchNormalization(name='Inputs_Normalization'))
        logger.debug('Add input layer with %d inputs to model %s', input_dim,
                     self.name)
        # Add hidden layers
        for i, layer_size in enumerate(self.layers):
            # Hidden layer
            model.add(
                keras.layers.Dense(layer_size,
                                   activation=self.hidden_activation,
                                   kernel_initializer=self.kernel_initializer,
                                   name=f"Layer_{i + 1}"))
            logger.debug('Add hidden layer #%d with %d units for model %s',
                         i + 1, layer_size, self.name)
            # Batch normalization
            if self.use_batch_normalization:
                model.add(
                    keras.layers.BatchNormalization(
                        name=f'Layer_{i + 1}_Normalization'))
                logger.debug(
                    'Add batch normalization after hidden layer #%d for model %s',
                    i + 1, self.name)
            # Dropout rate
            if 0.0 < self.dropout_rate < 1.0:
                model.add(
                    keras.layers.Dropout(rate=self.dropout_rate,
                                         name=f"Dropout_{i + 1}"))
                logger.debug(
                    'Add dropout after layer #%d with probability %f for model %s',
                    i + 1, self.dropout_rate, self.name)
        # Add output layer
        model.add(
            keras.layers.Dense(output_dim,
                               activation=self.output_activation,
                               name='Output'))
        logger.debug('Add output layer %d outputs for model %s', output_dim,
                     self.name)
        self.model = model
