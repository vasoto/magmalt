import pytest

from magmalt.data.builder import DatasetBuilder


@pytest.mark.data
def test_builder__init():
    builder = DatasetBuilder(dict(context=None))
    assert builder.context['context'] is None


class MyContext:
    datasets = dict()


@pytest.mark.data
def test_builder__build():
    config = dict(datasets=dict(dataset_foo=dict(features=['foo', 'bar']),
                                dataset_bar=dict(features=['bar', 'zap'])))
    context = MyContext()
    builder = DatasetBuilder(context)
    builder.build(config)
    assert context.datasets['dataset_foo'].features == set(['foo', 'bar'])
    assert context.datasets['dataset_bar'].features == set(['bar', 'zap'])
