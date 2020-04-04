import pytest

from magmalt.utils.features_mixin import FeaturesMixin, FeaturesParser


class TestFeatures(FeaturesMixin):
    test_features1 = ['feature1', 'my_feature']
    test_features2 = ['feature2', 'my_feature']
    test_features3 = 'feature3'  # String features field
    test_features4 = ['feature4']  # Single element features field
    features = ['your_feature']
    _feature_fields = [
        'test_features1', 'test_features2', 'test_features3', 'test_features4'
    ]


@pytest.mark.utils
def test_feature_mixin__get_features():
    obj = TestFeatures()
    assert len(obj.get_features()) == 5
    assert set(obj.get_features()) == set(
        ['feature1', 'my_feature', 'feature2', 'feature3', 'feature4'])


@pytest.mark.utils
def test_feature_mixin__features_parser():
    features = [
        '(MHillas_1.fSize > 30)or(MHillas_2.fSize > 30)',
        '(MHillas_1.fSize > 30)and(MHillas_2.fSize > 30)',
        'sqrt(MHillasTimeFit_2.fP1Grad*MHillasTimeFit_1.fP1Grad)',
        'log10(MHillas_2.fSize)'
    ]
    parser = FeaturesParser(features)
    parsed_features = parser.parse()
    assert set(parsed_features) == set([
        'MHillas_2.fSize', 'MHillas_1.fSize', 'MHillasTimeFit_1.fP1Grad',
        'MHillasTimeFit_2.fP1Grad'
    ])
