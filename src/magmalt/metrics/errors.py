from functools import partial
from sklearn.metrics import mean_absolute_error, \
    mean_squared_error, median_absolute_error

from magmalt.core import Metric


class MeanAbsoluteErrorMetric(Metric):
    """ Mean absolute error (MAE) metric
    """
    def __init__(self, context):
        super().__init__(name='MeanAbsoluteErrorMetric',
                         context=context,
                         score_func=mean_absolute_error)


class MeanSquaredErrorMetric(Metric):
    """ Mean squared error (MSE) metric
    """
    def __init__(self, context):
        super().__init__(name='MeanSquaredErrorMetric',
                         context=context,
                         score_func=mean_squared_error)


class RootMeanSquaredErrorMetric(Metric):
    """ Root mean squared error (RMSE) metric
    """
    def __init__(self, context):
        super().__init__(name='RootMeanSquaredErrorMetric',
                         context=context,
                         score_func=partial(mean_squared_error, squared=False))


class MedianAbsoluteErrorMetric(Metric):
    """ Median squared error (MedSE) metric
    """
    def __init__(self, context):
        super().__init__(name='MedianAbsoluteErrorMetric',
                         context=context,
                         score_func=median_absolute_error)
