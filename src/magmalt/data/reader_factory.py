from functools import partial
import logging
import os

from magmalt.data.reader.root_reader import RootReader
from magmalt.core import Factory

ReadersExtension = {'.root': RootReader}

Readers = dict(RootReader=RootReader)

logger = logging.getLogger('reader_factory')


class ReaderFactory(Factory):
    def __init__(self, context):
        super().__init__(context=context, config_section='datasets')

    def get_instance(self, dataset_name, dataset_config):
        logger.debug("Configure reader for dataset %s", dataset_name)
        reader = Readers.get(dataset_config.pop('reader', None), None)
        if reader is None:
            files = dataset_config.get('files', None)
            if files is None:
                raise ValueError(
                    "Neither of dataset properties 'files' nor 'reader' is "
                    f"set for dataset {dataset_name}")
            _, ext = os.path.splitext(files)
            if not ext:
                raise ValueError(f"Cannot extract file extension for {files}"
                                 f" for dataset {dataset_name}")
            reader = ReadersExtension.get(ext, None)
        if reader is None:
            raise ValueError("Cannot determine reader for dataset "
                             f"{dataset_name}")
        reader = partial(reader,
                         dataset=dataset_name,
                         name=f'read_{dataset_name}')
        return reader
