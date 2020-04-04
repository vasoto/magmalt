import glob
import logging

import pandas as pd
from tqdm import tqdm
import uproot

from magmalt.core import Step
from magmalt.utils.features_mixin import FeaturesParser

logger = logging.getLogger('root_reader')


class RootReader(Step):
    def __init__(self, name, context, tree, files, dataset, **kwargs):
        super().__init__(name=name, context=context)
        self.tree = tree
        self.files = files
        self.dataset = dataset
        self.nevents = -1

    def initialize(self):
        result = self.check_files()
        result &= self.set_nevents()

        return result

    def set_nevents(self):
        """ Try to enumerate the events in specified dataset
        """
        try:
            self.nevents = sum([
                uproot.numentries(root_file, treepath=self.tree)
                for root_file in glob.glob(self.files)
            ])
        except Exception as err:
            logger.error('Cannot enumerate all events for dataset %s: %s',
                         self.name, err)
            self.nevents = -1
            return False
        return True

    def check_files(self):
        """
        Check if files exist
        """
        files = glob.glob(self.files)
        if not files:
            logger.error("Reader %s cannot find files %s for dataset %s",
                         self.name, str(self.files), self.dataset)
            return False
        return True

    def get_branches(self):
        features = self.context.datasets[self.dataset].features

        branches = FeaturesParser(features).parse()
        return branches

    def _read_data(self):
        branches = self.get_branches()
        # Create data reader generator
        data_gen = uproot.iterate(self.files,
                                  treepath=self.tree,
                                  branches=branches,
                                  outputtype=pd.DataFrame,
                                  reportentries=True)
        # Create progress bar
        progress = tqdm(total=self.nevents, unit='events', unit_scale=True)
        chunks = []
        for start, stop, data_chunk in data_gen:
            progress.update(stop - start)
            chunks.append(data_chunk)
        progress.close()
        self.context.datasets[self.dataset].data = pd.concat(chunks,
                                                             ignore_index=True)

    def run(self):  # pragma: no cover
        try:
            self._read_data()
        except Exception as err:
            logging.error("Error while reading data for dataset %s: %s",
                          self.dataset, err)
            return False
        return True