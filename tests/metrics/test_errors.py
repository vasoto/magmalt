import pytest

from magmalt.metrics import MeanAbsoluteErrorMetric, MeanSquaredErrorMetric, \
    MedianAbsoluteErrorMetric, RootMeanSquaredErrorMetric


class MyModel:
    def predict(self, X):
        return X


class MyContext:
    models = dict()


@pytest.mark.metrics
def test_mae():
    context = MyContext()
    context.models['my_model'] = MyModel()

    metric = MeanAbsoluteErrorMetric(context)
    score = metric.score([1, 2, 3, 4, 5], [2, 4, 6, 8, 10])
    assert score == 3.0

    score = metric.score_model('my_model', [1, 2, 3, 4], [1, 2, 3, 4])
    assert score == 0.0


@pytest.mark.metrics
def test_mse():
    context = MyContext()
    context.models['my_model'] = MyModel()

    metric = MeanSquaredErrorMetric(context)
    score = metric.score([1, 2, 3, 4, 5], [2, 4, 6, 8, 10])
    assert score == 11.0

    score = metric.score_model('my_model', [1, 2, 3, 4], [1, 2, 3, 4])
    assert score == 0.0


@pytest.mark.metrics
def test_medae():
    context = MyContext()
    context.models['my_model'] = MyModel()

    metric = MedianAbsoluteErrorMetric(context)
    score = metric.score([3, -0.5, 2, 7], [2.5, 0.0, 2, 8])
    assert score == 0.5

    score = metric.score_model('my_model', [3, -0.5, 2, 7], [2.5, 0.0, 2, 8])
    assert score == 0.5


@pytest.mark.metrics
def test_rmse():
    context = MyContext()
    context.models['my_model'] = MyModel()

    metric = RootMeanSquaredErrorMetric(context)
    score = metric.score([3, -0.5, 2, 7], [2.5, 0.0, 2, 8])
    assert score == pytest.approx(0.612372435)

    score = metric.score_model('my_model', [3, -0.5, 2, 7], [2.5, 0.0, 2, 8])
    assert score == pytest.approx(0.612372435)
