from .errors import MeanAbsoluteErrorMetric, MeanSquaredErrorMetric, \
    MedianAbsoluteErrorMetric, RootMeanSquaredErrorMetric  # pragma: no cover

Metrics = dict(
    MAE=MeanAbsoluteErrorMetric,  # pragma: no cover
    MeanAbsoluteError=MeanAbsoluteErrorMetric,
    MSE=MeanSquaredErrorMetric,
    MeanSquaredError=MeanSquaredErrorMetric,
    MedAE=MedianAbsoluteErrorMetric,
    MedianAbsoluteError=MedianAbsoluteErrorMetric,
    RMSE=RootMeanSquaredErrorMetric,
    RootMeanSquaredError=RootMeanSquaredErrorMetric)
