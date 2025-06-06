"""Tests for sensor functionality."""
import pytest
from unittest.mock import Mock, patch
from src.sensor import DHT22Sensor, MockSensor, SensorReading


def test_sensor_reading_properties():
    """Test SensorReading properties."""
    reading = SensorReading(temperature=25.0, humidity=60.0, timestamp=1234567890)
    
    assert reading.temperature == 25.0
    assert reading.humidity == 60.0
    assert reading.temperature_f == 77.0  # (25 * 9/5) + 32


def test_mock_sensor():
    """Test mock sensor functionality."""
    sensor = MockSensor(temperature=22.0, humidity=45.0)
    reading = sensor.read()
    
    assert reading is not None
    assert reading.temperature == 22.0
    assert reading.humidity == 45.0
    assert reading.timestamp > 0


@patch('src.sensor.dht', None)
def test_dht22_sensor_mock_mode():
    """Test DHT22 sensor in mock mode (when Adafruit_DHT not available)."""
    sensor = DHT22Sensor(pin=4)
    reading = sensor.read()
    
    assert reading is not None
    assert isinstance(reading.temperature, float)
    assert isinstance(reading.humidity, float)


@patch('src.sensor.dht')
def test_dht22_sensor_successful_read(mock_dht_module):
    """Test successful DHT22 sensor read."""
    # Mock the DHT module
    mock_dht = Mock()
    mock_dht.DHT22 = 'DHT22'
    mock_dht.read_retry.return_value = (65.0, 24.5)  # humidity, temperature
    mock_dht_module.return_value = mock_dht
    
    with patch('src.sensor.dht', mock_dht):
        sensor = DHT22Sensor(pin=4)
        sensor.dht = mock_dht
        sensor.sensor_type = 'DHT22'
        
        reading = sensor.read()
        
        assert reading is not None
        assert reading.temperature == 24.5
        assert reading.humidity == 65.0


@patch('src.sensor.dht')
def test_dht22_sensor_retry_logic(mock_dht_module):
    """Test DHT22 sensor retry logic."""
    mock_dht = Mock()
    mock_dht.DHT22 = 'DHT22'
    # First two calls return None, third succeeds
    mock_dht.read_retry.side_effect = [
        (None, None), (None, None), (50.0, 23.0)
    ]
    mock_dht_module.return_value = mock_dht
    
    with patch('src.sensor.dht', mock_dht):
        sensor = DHT22Sensor(pin=4, max_retries=3)
        sensor.dht = mock_dht
        sensor.sensor_type = 'DHT22'
        
        reading = sensor.read()
        
        assert reading is not None
        assert reading.temperature == 23.0
        assert reading.humidity == 50.0
        assert mock_dht.read_retry.call_count == 3


@patch('src.sensor.dht')
def test_dht22_sensor_max_retries_exceeded(mock_dht_module):
    """Test DHT22 sensor when max retries exceeded."""
    mock_dht = Mock()
    mock_dht.DHT22 = 'DHT22'
    mock_dht.read_retry.return_value = (None, None)
    mock_dht_module.return_value = mock_dht
    
    with patch('src.sensor.dht', mock_dht):
        sensor = DHT22Sensor(pin=4, max_retries=2)
        sensor.dht = mock_dht
        sensor.sensor_type = 'DHT22'
        
        reading = sensor.read()
        
        assert reading is None
        assert mock_dht.read_retry.call_count == 2
