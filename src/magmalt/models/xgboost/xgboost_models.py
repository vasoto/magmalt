from magmalt.core import Model
from xgboost import XGBRegressor


class XGBoostRegressorModel(Model):
    def __init__(self, name, context, inputs, outputs, dataset, **kwargs):
        super().__init__(name=name,
                         context=context,
                         inputs=inputs,
                         outputs=outputs,
                         dataset=dataset)
        self.options = kwargs

    def create(self):
        self.model = XGBRegressor(**self.options)

    def train(self, X, y, **kwargs):
        self.model.fit(X, y, **kwargs)

    def predict(self, X, **kwargs):
        return self.model.predict(X, **kwargs)

    def predict_proba(self, X, **kwargs):
        return self.model.predict_proba(X, **kwargs)