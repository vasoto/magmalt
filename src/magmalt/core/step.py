
from magmalt.core import ContextAwareMixin


class Step(ContextAwareMixin):
    def __init__(self, name, context, **kwargs):
        super().__init__(context=context, name=name)
        self.options = kwargs

    def initialize(self): # pragma: no cover
        return True

    def run(self): # pragma: no cover
        return True

