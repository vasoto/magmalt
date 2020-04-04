from sklearn.base import TransformerMixin  # pragma: no cover


class BaseTransformer(TransformerMixin):  # pragma: no cover
    def fit(self, X, y, **kwargs):  # pragma: no cover
        pass

    def transform(self, X, **kwargs):  # pragma: no cover
        pass
