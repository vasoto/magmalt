from magmalt.utils.features_mixin import FeaturesMixin


class TestFeatures(FeaturesMixin):
    test_features1 = ['feature1', 'my_feature']
    test_features2 = ['feature2', 'my_feature']
    test_features3 = 'feature3'  # String features field
    test_features4 = ['feature4']  # Single element features field
    features = ['your_feature']
    _feature_fields = [
        'test_features1', 'test_features2', 'test_features3', 'test_features4'
    ]


def test_feature_mixin_get_features():
    obj = TestFeatures()
    assert len(obj.get_features()) == 5
    assert set(obj.get_features()) == set(
        ['feature1', 'my_feature', 'feature2', 'feature3', 'feature4'])
