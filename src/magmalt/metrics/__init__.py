from .errors import MeanAbsoluteErrorMetric, MeanSquaredErrorMetric, \
    MedianAbsoluteErrorMetric, RootMeanSquaredErrorMetric

Metrics = dict(MAE=MeanAbsoluteErrorMetric,
               MeanAbsoluteError=MeanAbsoluteErrorMetric,
               MSE=MeanSquaredErrorMetric,
               MeanSquaredError=MeanSquaredErrorMetric,
               MedAE=MedianAbsoluteErrorMetric,
               MedianAbsoluteError=MedianAbsoluteErrorMetric,
               RMSE=RootMeanSquaredErrorMetric,
               RootMeanSquaredError=RootMeanSquaredErrorMetric)
