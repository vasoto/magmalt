import logging
from magmalt.core.step import Step
from magmalt.utils.features_mixin import FeaturesMixin, FeaturesParser
from magmalt.utils.feature_context import SanitizedFeaturesContext

logger = logging.getLogger('MarsFilters')


class MarsFilters(Step, FeaturesMixin):
    def __init__(self, context, name, filters, datasets, **kwargs):
        super().__init__(context=context, name=name, **kwargs)
        self.filters = filters
        self.datasets = datasets
        self.features = []
        self._feature_fields = ['features']

    def _translate_filters(self):
        """ Translate features syntax from MARS/Root/C++ to Python/numexpr
        """
        self.filters = list(
            map(lambda a: a.replace('||', ' or ').replace('&&', ' and '),
                self.filters))
        logger.debug("Filters translated")
        self.features = []

    def _get_features(self):
        """ Extract features used in filters
        """
        return FeaturesParser(self.filters).parse()

    def initialize(self):
        logger.debug("Initializing filters ...")
        self._translate_filters()

        self.features = FeaturesParser(self.filters).parse()
        logger.debug("Filters parsed")
        for dataset_name in self.datasets:
            print("Dataset:", dataset_name)
            dataset = self.context.datasets[dataset_name]
            self.update_dataset_features(dataset)
        return True

    def run(self):
        for dataset_name in self.datasets:
            dataset = self.context.datasets[dataset_name]
            with SanitizedFeaturesContext(dataset) as context:
                count_before = context.data.shape[0]
                # Apply filters with one query
                filter_ = " & ".join(
                    [context.sanitize(f) for f in self.filters])
                logger.debug("Applying filter %s", filter_)
                context.data.query(filter_, inplace=True)
                # Check if data correctly referenced
                count_after = self.context.datasets[dataset_name].data.shape[0]
                logger.info(
                    "%d events left in dataset \"%s\" "
                    "after applying filters. %d events removed. "
                    "(Original size was %d)", count_after, dataset_name,
                    count_before - count_after, count_before)
        return True
