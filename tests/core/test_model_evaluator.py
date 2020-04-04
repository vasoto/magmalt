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
