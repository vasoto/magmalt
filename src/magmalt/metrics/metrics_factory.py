from typing import Dict, Any

from magmalt.core import Factory
from magmalt.metrics import Metrics


class MetricsFactory(Factory):
    def __init__(self, context):
        super().__init__(context=context, config_section='metrics')

    def get_instance(self, metric_name, metric_config):
        instance_cls = Metrics.get(metric_name, None)
        if instance_cls is None:
            raise ValueError(f"Cannot find metric {metric_name}")
        return instance_cls

    def create_step(self, step_name, step_conf):
        metrics_instance = self.get_instance(step_name, step_conf)
        if step_conf is None:
            step_conf = {}
        # Metrics' name is preset
        return metrics_instance(context=self.context, **step_conf)

    # def create_all(self, configuration: Dict[str, Any]):
    #     print(configuration)
    #     exit()
    #     super().create_all(configuration=configuration)
    #     return self