from sklearn.base import TransformerMixin

from magmalt.core import ContextAwareMixin


class BaseTransformer(TransformerMixin):
    def fit(self, X, y, **kwargs):
        pass

    def transform(self, X, **kwargs):
        pass
