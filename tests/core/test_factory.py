import pytest
from functools import partial
from magmalt.core import Factory


class MyStep:
    def __init__(self, context, name: str, foo=None):
        self.name = name
        self.context = context
        self.foo = foo


class MyFactory(Factory):
    def get_instance(self, name, config):
        if config and 'foo' in config:  # add some logic
            if config['foo'] is not None:
                return MyStep
            elif config['foo'] == 'partial':
                return partial(MyStep)
            else:
                raise ValueError("TestMessage")


def test_factory__init():
    factory = Factory(context=None, config_section='tests')
    assert factory.context is None
    assert factory.config_section == 'tests'
    assert factory.steps == []


def test_factory__get_instance():
    factory = Factory(None, '')
    with pytest.raises(NotImplementedError) as excinfo:
        factory.get_instance(name='test_name', config={})
        assert excinfo.value == "Method 'get_instance' is not defined"
    test_factory = MyFactory(None, '')
    assert test_factory.get_instance(None, None) == None
    assert test_factory.get_instance(None, {'foo': 1}) == MyStep


def test_factory__create_step():
    factory = MyFactory(context=dict(context=None), config_section='')
    step = factory.create_step(name='new step', step_config={'foo': 'bar'})
    assert step.name == 'new step'
    assert step.foo == 'bar'
    assert step.context['context'] is None

    with pytest.raises(ValueError) as excinfo:
        factory.create_step(name='new_step', step_config=dict(foo=None))
        assert excinfo.value == 'TestMessage'
    with pytest.raises(TypeError) as excinfo:
        factory.create_step(name='failing step', step_config=None)
        assert excinfo.value == "TypeError: 'NoneType' object is not callable"


data = dict(tests=dict(first_step=dict(foo='bar'), second_step=dict(
    foo='zap')))


def test_factory__create_all():
    factory = MyFactory(context=dict(context=None), config_section='tests')
    factory.create_all(data)
    assert len(factory.steps) == 2
    assert factory.steps[0].name == 'first_step'
    assert factory.steps[0].foo == 'bar'
    assert factory.steps[0].context['context'] is None

    assert factory.steps[1].name == 'second_step'
    assert factory.steps[1].foo == 'zap'
    assert factory.steps[1].context['context'] is None
