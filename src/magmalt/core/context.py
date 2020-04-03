from typing import Dict, Set, Any


class Context:
    """ This class represents a pipeline context.
    All steps of a pipeline get their data and set their results here 
    """
    def __init__(self):

        self.owner: Any = None
        self.datasets: Dict[str, Any] = dict()
        self.steps: Dict[str, Any] = dict()
        self.models: Dict[str, Any] = dict()


class ContextAwareMixin:
    def __init__(self, context, name):
        self.context = context
        self.name = name
