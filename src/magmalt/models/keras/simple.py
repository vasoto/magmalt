import logging

try:
    from tensorflow import keras
except Exception as _:
    import keras
    logging.warning('Upgrade Tensorflow!')

from magmalt.core import Model


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

    def _create_layer(self, prev_layer, layer_index, size):
        x = keras.layers.Dense(units=size,
                               activation=self.hidden_activation,
                               kernel_initializer=self.kernel_initializer,
                               name=f'Layer_{layer_index + 1}')(prev_layer)
        if self.use_batch_normalization:
            x = keras.layers.BatchNormalization(
                name=f'NormalizationLayer_{layer_index + 1}')(x)
        if 0.0 < self.dropout_rate < 1.0:
            x = keras.layers.Dropout(rate=self.dropout_rate,
                                     name=f"Dropout_{layer_index + 1}")(x)
        return x

    def create(self):
        input_dim = len(self.inputs)
        inputs = keras.layers.Input(shape=(input_dim), name='Inputs')
        x = inputs
        if self.use_batch_normalization:
            # Add batch normalization after the input layer
            x = keras.layers.BatchNormalization(name='NormalizationLayer')(x)
        for i, layer_size in enumerate(self.layers):
            x = self._create_layer(x, i, layer_size)

        # Add output
        outputs = keras.layers.Dense(
            len(self.outputs),
            activation=self.output_activation,
            kernel_initializer=self.kernel_initializer,
            name='Output')(x)
        self.model = keras.models.Model(inputs=[inputs], outputs=[outputs])
