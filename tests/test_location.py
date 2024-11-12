from unittest.mock import MagicMock
from unittest.mock import patch

from src.location import get_location

import pytest


@pytest.fixture
def mock_geocoder():
    with patch('src.location.geocoder', autospec=True) as mock:
        yield mock

@pytest.fixture
def sample_location_data():
    return {
        "ip": "8.8.8.8",
        "city": "Mountain View",
        "country": "US",
        "lat": 37.386,
        "lng": -122.0838,
        "state": "California"
    }

def test_get_location_success(mock_geocoder, sample_location_data):
    mock_location = MagicMock()
    mock_location.json = sample_location_data
    mock_geocoder.ip.return_value = mock_location

    result = get_location()

    assert result == sample_location_data
    mock_geocoder.ip.assert_called_once_with("me")


@pytest.fixture(autouse=True)
def _clear_cache():
    get_location.cache_clear()
    yield
    get_location.cache_clear()


def test_get_location_failure(mock_geocoder):
    mock_geocoder.ip.side_effect = Exception("Network error")

    result = get_location()

    assert result is None
    mock_geocoder.ip.assert_called_once_with("me")

def test_get_location_none_response(mock_geocoder):
    mock_location = MagicMock()
    mock_location.json = None
    mock_geocoder.ip.return_value = mock_location

    result = get_location()

    assert result is None
    mock_geocoder.ip.assert_called_once_with("me")
