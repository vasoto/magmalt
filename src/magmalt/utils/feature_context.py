import ast
from collections import OrderedDict
import logging
import re
from typing import Callable, OrderedDict as OrderedDictType

import numpy as np

from magmalt.core.dataset import Dataset

logger = logging.getLogger('feature_context')


def sanitize_column_name(column_name: str) -> str:
    """ This renames complex features and filters
    by replacing "." with "_"
    """
    regex = r"([a-zA-Z_][\w]+)\.([a-zA-Z_][\w]+)"
    subst = r"\1_\2"
    result = re.sub(regex, subst, column_name, 0,
                    re.VERBOSE | re.DOTALL | re.MULTILINE)
    return result


class SanitizedFeaturesContext:
    """ Some operations (e.g. apply, query) on data in pandas doesn't work
    with feautres containing '.' in the column name.
    This class tries to overcome this problem by renaming the column name
    and storing the orignal name which can be restored once all operations are
    completed.
    Example:
    # Apply
    with SanitizedFeaturesContext(dataset=context.datasts['energy]) as \
        data_context:
        for func in functions:
            try:
                sanitized_name = data_context.sanitize(func)
                context.data[sanitized_name] = data_context.data.apply(func)
            except Exception as err:
                logging.error("Could not apply function %s", func)
                raise err
            else:
                data_context.sanitized_features[sanitized_name] = func

    # Query
    with SanitizedFeaturesContext(dataset=context) as data_context:
        all_filters = ''
        filter_ = " && ".join([data_context.sanitize(f)
                                   for f in filters])
        data_context.query(filter_, inplace=True)

    In both examples, after exiting this context, the column names are resotred
    to the original.

    """
    def __init__(self,
                 dataset: Dataset,
                 sanitizer: Callable[[str], str] = sanitize_column_name):
        self.sanitized_features: OrderedDictType[str, str] = OrderedDict()
        self.dataset = dataset
        self.sanitizer = sanitizer

    @property
    def data(self):
        return self.dataset.data

    def _store(self) -> None:
        self.sanitized_features = OrderedDict()
        for column in self.dataset.data.columns:
            sanitized = self.sanitize(column)
            self.sanitized_features[sanitized] = column

    def sanitize(self, column_name: str) -> str:
        return self.sanitizer(column_name)

    def restore(self):
        self.data.columns = self.sanitized_features.values()

    def sanitize_all(self):
        self._store()
        self.data.columns = self.sanitized_features.keys()

    def __enter__(self):
        self.sanitize_all()
        return self

    def __exit__(self, type, value, traceback):
        self.restore()


class InputVisitor(ast.NodeVisitor):
    def __init__(self):
        self.container = None

    def visit_Name(self, node):
        if node.id != 'log10':
            self.container = node.id
        return node


def eval_features(dataset):
    with SanitizedFeaturesContext(dataset) as data_context:
        for feature in dataset.features:
            sanitized_name = data_context.sanitize(feature)
            if sanitized_name in data_context.data.columns:
                continue
            logger.debug("%s not found in dataset evaluating...",
                         sanitized_name)

            try:
                data_context.data[sanitized_name] = data_context.data.eval(
                    sanitized_name, parser='python', engine='numexpr')
            except ValueError as err:
                if 'log10' in feature:
                    visitor = InputVisitor()
                    visitor.visit(ast.parse(sanitized_name))
                    param_name = visitor.container
                    data_context.data[sanitized_name] = np.log10(
                        data_context.data[param_name])
                else:
                    continue
            else:
                data_context.sanitized_features[sanitized_name] = feature
