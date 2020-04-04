import pytest

from magmalt.metrics.metrics_factory import MetricsFactory
from magmalt.metrics import Metrics, MeanAbsoluteErrorMetric, MedianAbsoluteErrorMetric


@pytest.mark.metrics
def test_metrics_factory__init():
    factory = MetricsFactory(None)
    assert factory.context is None
    assert factory.config_section == 'metrics'


@pytest.mark.metrics
def test_metrics_factory__get_instance():
    factory = MetricsFactory(None)
    instances = [factory.get_instance(metric) for metric in Metrics.keys()]
    assert instances == list(Metrics.values())

    with pytest.raises(ValueError, match="Cannot find metric Test Metric"):
        factory.get_instance('Test Metric')


@pytest.mark.metrics
def test_metrics_factory__create_step():
    factory = MetricsFactory(None)
    instance = factory.create_step('MAE', None)
    assert isinstance(instance, MeanAbsoluteErrorMetric)

    instance = factory.create_step('MedAE', {})
    assert isinstance(instance, MedianAbsoluteErrorMetric)
