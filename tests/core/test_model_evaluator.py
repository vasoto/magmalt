import pytest

from magmalt.core.model_evaluator import ModelEvaluator


@pytest.mark.core
def test_model_evaluator__init():
    evaluator = ModelEvaluator('test evaluator', {'context': None},
                               'my_model',
                               'my_dataset',
                               'my_results',
                               foo='bar')
    assert evaluator.context['context'] is None
    assert evaluator.name == 'test evaluator'
    assert evaluator.model == 'my_model'
    assert evaluator.dataset == 'my_dataset'
    assert evaluator.results == 'my_results'


class MyContext:
    models = dict()
    datasets = dict()


class MyModel:
    def update_dataset_features(self, dataset):
        dataset.features = ['foo', 'bar']


class MyDataset:
    features = []
    data = None


@pytest.mark.core
def test_model_evaluator__initialize():
    model = MyModel()
    dataset = MyDataset()
    context = MyContext()
    context.models['my_model'] = model
    context.datasets['my_dataset'] = dataset
    evaluator = ModelEvaluator('test evaluator',
                               context=context,
                               model='my_model',
                               dataset='my_dataset',
                               results='my_results')
    assert evaluator.initialize()
    assert dataset.features == ['foo', 'bar']


@pytest.mark.core
def test_model_evaluator__evaluate():
    model = MyModel()
    dataset = MyDataset()
    dataset.data = list(range(5))
    context = MyContext()
    context.models['my_model'] = model
    context.datasets['my_dataset'] = dataset
    evaluator = ModelEvaluator('test evaluator',
                               context=context,
                               model='my_model',
                               dataset='my_dataset',
                               results='my_results')
    evaluator.evaluate()
    assert context.datasets['my_results'].data == [0, 1, 2, 3, 4]


@pytest.mark.core
def test_model_evaluator__run():
    model = MyModel()
    dataset = MyDataset()
    dataset.data = list(range(5))
    context = MyContext()
    context.models['my_model'] = model
    context.datasets['my_dataset'] = dataset
    evaluator = ModelEvaluator('test evaluator',
                               context=context,
                               model='my_model',
                               dataset='my_dataset',
                               results='my_results')
    evaluator.run()
    assert context.datasets['my_results'].data == [0, 1, 2, 3, 4]
