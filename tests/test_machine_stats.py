import pytest
from unittest.mock import patch, Mock
import psutil 
from src.machine_stats import get_stats_sensors


def test_get_stats_sensors_all_available():
    """Test when all sensors are available"""
    with patch('src.machine_stats.psutil') as mock_psutil:  
        # Setup mocks
        mock_psutil.sensors_fans.return_value = {'cpu_fan': [Mock(current=1500)]}
        mock_psutil.sensors_temperatures.return_value = {'cpu_temp': [Mock(current=45.0)]}
        mock_psutil.sensors_battery.return_value = Mock(percent=75.5, power_plugged=True)

        result = get_stats_sensors()

        assert 'fans' in result
        assert 'temperatures' in result
        assert 'battery_percent' in result
        assert 'battery_power_plugged' in result
        assert result['battery_percent'] == 75.5
        assert result['battery_power_plugged'] is True

def test_get_stats_sensors_no_fans():
    """Test when fans are not available"""
    with patch('src.machine_stats.psutil') as mock_psutil:  
        # Setup mocks
        mock_psutil.sensors_fans.side_effect = AttributeError()
        mock_psutil.sensors_temperatures.return_value = {'cpu_temp': [Mock(current=45.0)]}
        mock_psutil.sensors_battery.return_value = Mock(percent=75.5, power_plugged=True)

        result = get_stats_sensors()

        assert 'fans' not in result
        assert 'temperatures' in result
        assert 'battery_percent' in result

def test_get_stats_sensors_no_temperatures():
    """Test when temperatures are not available"""
    with patch('src.machine_stats.psutil') as mock_psutil:  
        mock_psutil.sensors_fans.return_value = {'cpu_fan': [Mock(current=1500)]}
        mock_psutil.sensors_temperatures.side_effect = AttributeError()
        mock_psutil.sensors_battery.return_value = Mock(percent=75.5, power_plugged=True)

        result = get_stats_sensors()

        assert 'fans' in result
        assert 'temperatures' not in result
        assert 'battery_percent' in result

def test_get_stats_sensors_no_battery():
    """Test when battery is not available"""
    with patch('src.machine_stats.psutil') as mock_psutil:  
        mock_psutil.sensors_fans.return_value = {'cpu_fan': [Mock(current=1500)]}
        mock_psutil.sensors_temperatures.return_value = {'cpu_temp': [Mock(current=45.0)]}
        mock_psutil.sensors_battery.side_effect = AttributeError()

        result = get_stats_sensors()

        assert 'fans' in result
        assert 'temperatures' in result
        assert 'battery_percent' not in result
        assert 'battery_power_plugged' not in result

def test_get_stats_sensors_empty_temperatures():
    """Test when temperatures dict is empty"""
    with patch('src.machine_stats.psutil') as mock_psutil:  
        mock_psutil.sensors_fans.return_value = {'cpu_fan': [Mock(current=1500)]}
        mock_psutil.sensors_temperatures.return_value = {}
        mock_psutil.sensors_battery.return_value = Mock(percent=75.5, power_plugged=True)

        result = get_stats_sensors()

        assert 'fans' in result
        assert result['temperatures'] == {}
        assert 'battery_percent' in result