import glob

import pytest
import uproot
import pandas as pd

from magmalt.data.reader.root_reader import RootReader


def mock_glob_no_files(a: str):
    return None


def mock_glob_files(a: str):
    return [10, 20]


def uproot_numentries(a, treepath):
    return a


def mock_uproot_iterate(files, treepath, branches, outputtype, reportentries):
    return [(0, 1,
             pd.DataFrame([['a', 1], ['b', 2]], columns=['letter', 'number'])),
            (2, 3,
             pd.DataFrame([['c', 3], ['d', 4]], columns=['letter', 'number']))]


@pytest.mark.data
def test_root_reader__init():
    reader = RootReader(name='test_root_reader',
                        context=dict(context=None),
                        tree='TestTree',
                        files='TestFiles*.root',
                        dataset='TestDataset')
    assert reader.name == 'test_root_reader'
    assert reader.tree == 'TestTree'
    assert reader.files == 'TestFiles*.root'
    assert reader.dataset == 'TestDataset'
    assert reader.nevents == -1


@pytest.mark.data
def test_root_reader_check_files(monkeypatch):
    reader = RootReader(name='test_root_reader',
                        context=dict(context=None),
                        tree='TestTree',
                        files='TestFiles*.root',
                        dataset='TestDataset')

    monkeypatch.setattr(glob, 'glob', mock_glob_files)
    assert reader.check_files()

    monkeypatch.setattr(glob, 'glob', mock_glob_no_files)
    assert not reader.check_files()


@pytest.mark.data
def test_root_reader_set_nevents(monkeypatch):
    reader = RootReader(name='test_root_reader',
                        context=dict(context=None),
                        tree='TestTree',
                        files='TestFiles*.root',
                        dataset='TestDataset')

    monkeypatch.setattr(uproot, 'numentries', uproot_numentries)
    monkeypatch.setattr(glob, 'glob', mock_glob_files)
    assert reader.set_nevents()
    assert reader.nevents == 30

    monkeypatch.setattr(glob, 'glob', mock_glob_no_files)
    assert not reader.set_nevents()
    assert reader.nevents == -1


@pytest.mark.data
def test_root_reader__initialize(monkeypatch):
    reader = RootReader(name='test_root_reader',
                        context=dict(context=None),
                        tree='TestTree',
                        files='TestFiles*.root',
                        dataset='TestDataset')
    monkeypatch.setattr(uproot, 'numentries', uproot_numentries)
    monkeypatch.setattr(glob, 'glob', mock_glob_files)
    assert reader.initialize()
    assert reader.nevents == 30  # side effect

    monkeypatch.setattr(glob, 'glob', mock_glob_no_files)
    assert not reader.initialize()
    assert reader.nevents == -1


class MyDataset:
    features = []
    data = None


class MyContext:
    datasets = dict()


@pytest.mark.data
def test_root_reader__get_branches():
    context = MyContext()
    dataset = MyDataset()
    dataset.features = [
        '(MHillas_1.fSize > 30)or(MHillas_2.fSize > 30)',
        '(MHillas_1.fSize > 30)and(MHillas_2.fSize > 30)',
        'sqrt(MHillasTimeFit_2.fP1Grad*MHillasTimeFit_2.fP1Grad)',
        'log10(MHillas_2.fSize)'
    ]
    context.datasets['TestDataset'] = dataset
    reader = RootReader(name='test_root_reader',
                        context=context,
                        tree='TestTree',
                        files='TestFiles*.root',
                        dataset='TestDataset')
    branches = reader.get_branches()
    assert set(branches) == set([
        'MHillas_1.fSize', 'MHillas_2.fSize', 'MHillasTimeFit_2.fP1Grad',
        'MHillasTimeFit_2.fP1Grad'
    ])


@pytest.mark.data
def test_root_reader___read_data(monkeypatch):
    context = MyContext()
    dataset = MyDataset()
    dataset.features = [
        '(MHillas_1.fSize > 30)or(MHillas_2.fSize > 30)',
        '(MHillas_1.fSize > 30)and(MHillas_2.fSize > 30)',
        'sqrt(MHillasTimeFit_2.fP1Grad*MHillasTimeFit_2.fP1Grad)',
        'log10(MHillas_2.fSize)'
    ]
    context.datasets['TestDataset'] = dataset

    reader = RootReader(name='test_root_reader',
                        context=context,
                        tree='TestTree',
                        files='TestFiles*.root',
                        dataset='TestDataset')
    monkeypatch.setattr(uproot, 'iterate', mock_uproot_iterate)
    # monkeypatch.setattr(glob, 'glob', mock_glob_files)
    reader.nevents = 2
    reader._read_data()
    assert dataset.data.columns.tolist() == ['letter', 'number']
    assert dataset.data.letter.tolist() == ['a', 'b', 'c', 'd']
    assert dataset.data.number.tolist() == [1, 2, 3, 4]


@pytest.mark.data
def test_root_reader___eval_features(monkeypatch):
    context = MyContext()
    dataset = MyDataset()
    dataset.features = ['index*a', 'b/index', 'log(b)']
    dataset.data = pd.DataFrame([[1, 3, 6], [2, 4, 8], [3, 8, 16]],
                                columns=['index', 'a', 'b'])

    context.datasets['TestDataset'] = dataset
    reader = RootReader(name='test_root_reader',
                        context=context,
                        tree='TestTree',
                        files='TestFiles*.root',
                        dataset='TestDataset')
    reader._eval_features()
    assert context.datasets['TestDataset'].data['index*a'].tolist() == [
        3, 8, 24
    ]
    assert context.datasets['TestDataset'].data['b/index'].tolist() == [
        6.0, 4.0, 5.333333333333333
    ]
    assert context.datasets['TestDataset'].data['log(b)'].tolist() == [
        1.791759469228055, 2.0794415416798357, 2.772588722239781
    ]
