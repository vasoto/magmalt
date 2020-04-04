import pytest

from magmalt.core import Model


class MyContext:
    datasets = dict()


class MyDataset:
    features = []


@pytest.mark.core
def test_model__init():
    model = Model(name='test model',
                  context=None,
                  inputs=['input1', 'input2', 'input3'],
                  outputs=['target1', 'target2'],
                  dataset='my_dataset')
    assert model.context is None
    assert model.inputs == ['input1', 'input2', 'input3']
    assert model.outputs == ['target1', 'target2']
    assert model.dataset == 'my_dataset'
    assert model._feature_fields == ['inputs', 'outputs']


@pytest.mark.core
def test_model__initialize():
    context = MyContext()
    context.datasets['my_dataset'] = MyDataset()
    model = Model(name='test model',
                  context=context,
                  inputs=['input1', 'input2', 'input3'],
                  outputs=['target1', 'target2'],
                  dataset='my_dataset')
    model.initialize()
    assert context.datasets['my_dataset'].features == set(
        ['input1', 'input2', 'input3', 'target1', 'target2'])
