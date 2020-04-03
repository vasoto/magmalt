from typing import Dict, List, Union, Set, TypeVar, Any, Optional, Type
from pydantic import BaseModel
from pandas import DataFrame
from numpy import array

DataType = TypeVar('DataType', DataFrame, List, Dict, array)


class Dataset(BaseModel):
    """ Simple representation of a dataset
    name: dataset name
    features: union of all features used in models
    data: data container
    """
    name: str = ''
    features: Set[str] = set()
    data: Any = None  # DataType #TODO: Add validator for pandas.DataFrame
