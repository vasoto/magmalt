from .keras.simple import KerasSimpleModel
from .xgboost.xgboost_models import XGBoostRegressorModel

Models = dict(KerasSimpleModel=KerasSimpleModel,
              XGBoostRegressorModel=XGBoostRegressorModel)
