from .preprocessing.mars_filter import MarsFilters
from .preprocessing import MinMaxScaler, InverseScaler
from .models.trainers import KerasModelTrainer, XGBoostModelTrainer
from .core.model_evaluator import ModelEvaluator

Instances = dict(MarsFilters=MarsFilters,
                 MinMaxScaler=MinMaxScaler,
                 KerasModelTrainer=KerasModelTrainer,
                 XGBoostModelTrainer=XGBoostModelTrainer,
                 ModelEvaluator=ModelEvaluator,
                 InverseScaler=InverseScaler)
