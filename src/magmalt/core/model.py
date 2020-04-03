from magmalt.core import ContextAwareMixin, Step
from magmalt.utils.features_mixin import FeaturesMixin


class Model(ContextAwareMixin, FeaturesMixin):
    def __init__(self, name, context, inputs, outputs, dataset):
        super().__init__(name=name, context=context)
        self.inputs = inputs
        self.outputs = outputs
        self.dataset = dataset
        self._feature_fields = ['inputs', 'outputs']

    def initialize(self):
        dataset = self.context.datasets[self.dataset]
        self.update_dataset_features(dataset)
        self.create()

    def create(self):
        pass
