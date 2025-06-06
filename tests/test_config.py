"""Tests for temperature sensor configuration."""
import pytest
from unittest.mock import patch
from src.config import AppConfig, get_config


def test_app_config_defaults():
    """Test default configuration values."""
    with patch.dict('os.environ', {}, clear=True):
        config = AppConfig()
        
        assert config.sensor.pin == 4
        assert config.sensor.read_interval == 300
        assert config.sensor.metric_units is True
        assert config.sensor.max_retries == 3


def test_app_config_env_override():
    """Test environment variable override."""
    env_vars = {
        'SENSOR_PIN': '18',
        'SENSOR_READ_INTERVAL': '600',
        'SENSOR_METRIC_UNITS': 'false',
        'MQTT_SERVER': 'test.broker.com',
        'MQTT_USERNAME': 'testuser',
        'MQTT_PASSWORD': 'testpass'
    }
    
    with patch.dict('os.environ', env_vars, clear=True):
        config = AppConfig()
        
        assert config.sensor.pin == 18
        assert config.sensor.read_interval == 600
        assert config.sensor.metric_units is False
        assert config.mqtt.server == 'test.broker.com'
        assert config.mqtt.username == 'testuser'
        assert config.mqtt.password == 'testpass'


def test_device_mapping():
    """Test device configuration mapping."""
    config = AppConfig()
    
    # Check that all expected devices are configured
    expected_devices = [
        'raspberrypi-0w1', 'raspberrypi-0w2', 
        'raspberrypi-0w3', 'raspberrypi-0w4'
    ]
    
    for device in expected_devices:
        assert device in config.devices
        device_config = config.devices[device]
        assert device_config.location
        assert device_config.mqtt_temp_topic
        assert device_config.mqtt_humid_topic


@patch('socket.gethostname')
def test_current_device(mock_hostname):
    """Test current device detection."""
    mock_hostname.return_value = 'raspberrypi-0w1'
    config = AppConfig()
    
    current = config.current_device
    assert current.location == 'office'
    assert 'office' in current.mqtt_temp_topic


@patch('socket.gethostname')
def test_unknown_hostname_raises_error(mock_hostname):
    """Test that unknown hostname raises ValueError."""
    mock_hostname.return_value = 'unknown-device'
    config = AppConfig()
    
    with pytest.raises(ValueError, match="Unknown hostname"):
        _ = config.current_device
