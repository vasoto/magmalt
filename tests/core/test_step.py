import pytest

from magmalt.core import Step


@pytest.mark.core
def test_step__init():
    step = Step('test_step', dict(context=None), foo='bar')
    assert step.name == 'test_step'
    assert step.context['context'] == None
    assert step.options['foo'] == 'bar'
