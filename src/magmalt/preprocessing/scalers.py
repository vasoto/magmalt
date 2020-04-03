import logging
from typing import List, NoReturn, Dict, Any

from sklearn.preprocessing import MinMaxScaler as MinMaxScaler_
import pandas as pd
from pydantic import BaseModel

from magmalt.core.step import Step
from magmalt.utils.features_mixin import FeaturesMixin, FeaturesParser

logger = logging.getLogger('scalers')


class ScalerStep(Step):
    """ Scaling data base step class
    """
    def __init__(self, name: str, context, datasets: List[str], **kwargs):
        super().__init__(context=context, name=name, **kwargs)
        self.datasets = datasets

    def scale(self, data):
        pass

    def inverse_scale(self, dataset_name):
        pass

    def save_params(self, dataset_name: str, **kwargs):
        pass

    def run(self):
        for dataset_name in self.datasets:
            logging.debug("Scaling dataset %s", dataset_name)
            dataset = self.context.datasets[dataset_name]
            columns = dataset.data.columns
            dataset.data = pd.DataFrame(self.scale(dataset.data),
                                        columns=columns)
            self.save_params(dataset_name)
        return True


class InverseScaler(Step):
    def __init__(self, name: str, context, dataset: str, results: str,
                 scaler_step: str, scaled_dataset: str):
        super().__init__(name=name, context=context)
        self.dataset = dataset
        self.results = results
        self.scaler_step = scaler_step
        self.scaled_dataset = scaled_dataset

    def run(self):
        logging.debug(
            "Store inverse scaled data from dataset %s into dataset %s",
            self.scaled_dataset, self.results)
        # scaler_data = self.context.steps[self.scaler_step]
        if not self.dataset in self.context.datasets:
            logger.error("Missing dataset '%s'. Cannot perform step %s",
                         self.dataset, self.name)
            return False
        data = self.context.datasets[self.dataset].data
        # Get scaler step instance from pipeline
        scaler = self.context.owner.steps[self.scaler_step]
        # Inverse scale the data
        self.context.datasets[self.results] = scaler.inverse_scale(
            dataset_name=self.scaled_dataset, data=data)
        return True


class MinMaxScalerConfig(BaseModel):
    mins: Dict[str, float] = {}
    scale: Dict[str, float] = {}


class MinMaxScaler(ScalerStep):
    def __init__(
        self,
        context,
        name,
        datasets,
        min=0,
        max=1,
        copy=False,
    ):
        super().__init__(context=context, name=name, datasets=datasets)
        self.scaler = MinMaxScaler_(feature_range=(min, max), copy=copy)

    def save_params(self, dataset_name: str):
        logger.debug("Saving MinMax scaler parameters for dataset %s",
                     dataset_name)
        scaler_params = self.context.steps[self.name][dataset_name]

        columns = self.context.datasets[dataset_name].data.columns
        scaler_params.mins = dict(zip(columns, self.scaler.min_))
        scaler_params.scale = dict(zip(columns, self.scaler.scale_))
        scaler_params

    def scale(self, data):
        return self.scaler.fit_transform(dataset.data)

    def inverse_scale(self, dataset_name, data):
        params = self.context.steps[self.name][dataset_name]
        columns = data.columns
        self.scaler.scale_, self.scaler.min_ = zip(*((params.scale[col],
                                                      params.mins[col])
                                                     for col in columns))
        return pd.DataFrame(self.scaler.inverse_transform(data),
                            columns=columns)

    def initialize(self):
        logger.debug("Initialize MinMaxScaler %s", self.name)
        self.context.steps[self.name] = {
            dataset_name: MinMaxScalerConfig()
            for dataset_name in self.datasets
        }
        return True

    def run(self):
        for dataset_name in self.datasets:
            logger.info("Applying MinMax scaler to dataset %s", dataset_name)

            dataset = self.context.datasets[dataset_name]
            columns = dataset.data.columns
            dataset.data = pd.DataFrame(self.scaler.fit_transform(
                dataset.data),
                                        columns=columns)
            self.save_params(dataset_name)
        return True
