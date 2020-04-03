from typing import Iterable, Union, Callable, Optional

from .context import ContextAwareMixin

ScoreResult = Union[Iterable, float]
ScoreFunction = Callable[[Iterable, Iterable], Union[Iterable, float]]


class Metric(ContextAwareMixin):
    def __init__(self, name, context, score_func: ScoreFunction):
        super().__init__(name=name, context=context)
        self.score_func = score_func

    def score(self, y_true: Iterable, y_predicted: Iterable,
              **kwargs) -> ScoreResult:
        return self.score_func(y_true, y_predicted, **kwargs)

    def score_model(self,
                    model_name: str,
                    X: Iterable,
                    y_true: Iterable,
                    axis: Optional[int] = None,
                    **kwargs) -> ScoreResult:
        y_predicted = self.context.models[model_name].predict(X)
        if axis:
            y_predicted = y_predicted[:axis]
        return self.score(y_true, y_predicted)
