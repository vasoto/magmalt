from magmalt.core import Context, ContextAwareMixin


class ContextAwareMixinTest(ContextAwareMixin):
    def __init__(self, context):
        super().__init__(context=context, name='test_class')


def test_context_init():
    c = Context()
    assert c.steps == {}
    assert c.datasets == {}
    assert c.models == {}
    assert c.owner is None


def test_context_aware():
    c = ContextAwareMixinTest(Context())
    assert c.name == 'test_class'
