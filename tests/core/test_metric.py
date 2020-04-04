import pytest

from magmalt.core import Metric


def my_score_func(a, b):
    return [b[i] == e for i, e in enumerate(a)]


class MyModel:
    def predict(self, a):
        return [i**2 for i in a]


class MyContext:
    def __init__(self):
        self.models = dict(my_model=MyModel())


@pytest.mark.core
def test_metric__init():
    context = MyContext()
    metric = Metric('TestMetric', context=context, score_func=my_score_func)
    assert metric.name == 'TestMetric'
    assert metric.context == context
    assert metric.score_func == my_score_func


@pytest.mark.core
def test_metric__score():
    context = MyContext()
    metric = Metric('TestMetric', context=context, score_func=my_score_func)
    assert all(metric.score([1, 2, 3, 4], [1, 2, 3, 4]))


@pytest.mark.core
def test_metric__score_model():
    context = MyContext()
    metric = Metric('TestMetric', context=context, score_func=my_score_func)
    result = metric.score_model(model_name='my_model',
                                X=[1, 2, 3, 4],
                                y_true=[1, 4, 9, 16])
    assert all(result)

    result = metric.score_model(model_name='my_model',
                                X=[1, 2, 3, 4],
                                y_true=[1, 4, 9],
                                axis=-1)
    assert all(result)