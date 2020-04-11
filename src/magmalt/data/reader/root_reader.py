import glob
import logging

import pandas as pd
from tqdm import tqdm
import uproot

from magmalt.core import Step
from magmalt.utils.features_mixin import FeaturesParser
from magmalt.utils.feature_context import eval_features

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
        """ Extract ROOT branches from features

        Features could include complex functions or combinations of branches.
        So we need to extract all branches included in those complex features.
        """
        features = self.context.datasets[self.dataset].features
        return FeaturesParser(features).parse()

    def _read_data(self):
        # Extract all branches
        branches = self.get_branches()
        # Create upROOT data reader generator
        data_gen = uproot.iterate(self.files,
                                  treepath=self.tree,
                                  branches=branches,
                                  outputtype=pd.DataFrame,
                                  reportentries=True)
        # Create tqdm visual progress bar
        progress = tqdm(total=self.nevents, unit='events', unit_scale=True)
        chunks = []  # will hold extracted Pandas' DataFrame objects
        # Loop over ROOT file data
        for start, stop, data_chunk in data_gen:
            progress.update(stop - start)
            chunks.append(data_chunk)
        # Concatenate all DataFrames into one
        self.context.datasets[self.dataset].data = pd.concat(chunks,
                                                             ignore_index=True)
        progress.close()

    def _eval_features(self):
        """ Evaluate complex features

        Applies functions and/or complex relations
        between features
        """
        dataset = self.context.datasets[self.dataset]
        eval_features(dataset)

    def run(self):  # pragma: no cover
        """ Perform data readout from ROOT files
        """
        try:
            self._read_data()
            # Create complex features
            self._eval_features()
        except Exception as err:
            logging.error("Error while reading data for dataset %s: %s",
                          self.dataset, err)
            return False
        return True
