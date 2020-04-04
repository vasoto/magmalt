import ast
import logging
from typing import List
# from magmalt.core import Dataset


class GenericVisitor(ast.NodeVisitor):
    def __init__(self, container):
        self.container = container

    def visit_Attribute(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        self.container.append(f"{node.value.id}.{node.attr}")
        return node


class FeaturesParser:
    def __init__(self, features):
        self.features = features
        self.container = list()

    def parse(self):
        for feature in self.features:
            try:
                tree = ast.parse(feature)
                GenericVisitor(self.container).visit(tree)
            except Exception as err:
                logging.error('Cannot parse feature %s. Error: %s', feature,
                              err)
        return list(set(self.container))


class FeaturesMixin:
    """ Mixin to automatically add features to be read from data
    """
    _feature_fields: List[str] = []

    # def __init__(self, feature_fields):
    #     super().__init__(context=context)
    #      =

    def _enumerate_values(self):
        values = []
        for field_name in self._feature_fields:
            # Extract values from feature field
            value = getattr(self, field_name)
            # Handle strings
            if isinstance(value, str):
                value = [value]
            # TODO: Flatten lists of lists. Use case?
            values += value
        return values

    def get_features(self):
        """ Return extracted features
        """
        return list(set(self._enumerate_values()))

    def update_dataset_features(self, dataset: "Dataset") -> "Dataset":
        dataset.features = set(
            list(dataset.features) + self._enumerate_values())
        return dataset
