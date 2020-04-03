from typing import Dict, List, Union, Set, TypeVar, Any, Optional, Type
from pydantic import BaseModel
from pandas import DataFrame
from numpy import array

DataType = TypeVar('DataType', DataFrame, List, Dict, array)


class DatasetMetadata(BaseModel):
    # features: Set[str] = {}
    pass


class Dataset(BaseModel):
    """ Simple representation of a dataset
    name: dataset name
    features: union of all features used in models
    data: data container
    meta: additional information about the dataset. For example for root
          dataset might include information like tree name, additional features
          and feature aliases
    """
    name: str = ''
    features: Set[str] = set()
    data: Any = None  # DataType #TODO: Add validator for pandas.DataFrame
    meta: Optional[TypeVar(DatasetMetadata)]


class RootMetadata(DatasetMetadata):
    """ Root dataset should contains more feature information than the features
    needed only in the model (e.g. features used in filters).

    Also features extracted from a .root file, contain the name of the branch
    and the field in the branch separated by '.', so we need to
    rename those in order to have valid column names for some pandas 
    operations (eval, query).

    This data class stores the full set of features (branches) needed: `branches`
    and the mapping for renaming the original features to pandas-compatible
    ones: `feature_aliases`.
    `nevents` is the optional number of events in dataset

    Note: the easiest solution is to extract full information from .root file,
    instead fo trying to find all the features needed.
    But  sometimes this is not possible using uproot, also the full information is
    usually much more than what is needed in the models.
    """
    tree: str
    branches: Set[str] = {}
    feature_aliases: Dict[str, str] = {}
    nevents: int = -1
