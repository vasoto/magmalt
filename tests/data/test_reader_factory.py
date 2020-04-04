import pytest

from magmalt.data.reader_factory import ReaderFactory


@pytest.mark.data
def test_reader_factory__init():
    factory = ReaderFactory(dict(context=None))
    assert factory.config_section == 'datasets'
    assert factory.context['context'] is None


my_dataset = dict(reader='RootReader')
other_dataset = dict(files='some_file.root')


@pytest.mark.data
def test_reader_factory__get_instance_from_reader():
    factory = ReaderFactory(dict(context=None))
    instance = factory.get_instance('my_dataset', my_dataset)
    # .func because instance is a partial
    assert instance.func.__name__ == 'RootReader'


@pytest.mark.data
def test_reader_factory__get_instance_from_files():
    factory = ReaderFactory(dict(context=None))
    instance = factory.get_instance('other_dataset', other_dataset)
    # .func because instance is a partial
    assert instance.func.__name__ == 'RootReader'


@pytest.mark.data
def test_reader_factory__get_instance_exceptions():
    factory = ReaderFactory(dict(context=None))

    with pytest.raises(ValueError) as excinfo:
        factory.get_instance('empty_config', {})
        assert excinfo.value == "ValueError: Neither of dataset properties 'files' nor 'reader' is set for dataset empty_config"

    with pytest.raises(ValueError) as excinfo:
        factory.get_instance('no_extension',
                             {'files': 'file_name_without_extension'})
        assert excinfo.value == "ValueError: Cannot extract file extension for file_name_without_extension for dataset no_extension"

    with pytest.raises(ValueError) as excinfo:
        factory.get_instance('unknown_extension', {'files': 'file.ext'})
        assert excinfo.value == "ValueError: Cannot determine reader for dataset unknown_extension"
