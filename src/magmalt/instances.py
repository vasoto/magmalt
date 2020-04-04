from .preprocessing.mars_filter import MarsFilters  # pragma: no cover
from .preprocessing import MinMaxScaler, InverseScaler  # pragma: no cover
from .models.trainers import KerasModelTrainer, XGBoostModelTrainer  # pragma: no cover
from .core.model_evaluator import ModelEvaluator  # pragma: no cover

Instances = dict(  # pragma: no cover
    MarsFilters=MarsFilters,
    MinMaxScaler=MinMaxScaler,
    KerasModelTrainer=KerasModelTrainer,
    XGBoostModelTrainer=XGBoostModelTrainer,
    ModelEvaluator=ModelEvaluator,
    InverseScaler=InverseScaler)
