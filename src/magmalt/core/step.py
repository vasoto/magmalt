
from magmalt.core import ContextAwareMixin


class Step(ContextAwareMixin):
    def __init__(self, context, name, **kwargs):
        super().__init__(context=context, name=name)
        self.options = kwargs

    def initialize(self):
        return True

    def run(self):
        return True

