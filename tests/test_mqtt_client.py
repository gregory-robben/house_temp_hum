"""Tests for MQTT client functionality."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.mqtt_client import MQTTPublisher
from src.config import MQTTConfig


@pytest.fixture
def mqtt_config():
    """Create test MQTT configuration."""
    return MQTTConfig(
        server="test.broker.com",
        port=1883,
        username="testuser",
        password="testpass",
        use_tls=True
    )


@patch('src.mqtt_client.mqtt.Client')
def test_mqtt_publisher_init(mock_client_class, mqtt_config):
    """Test MQTT publisher initialization."""
    mock_client = Mock()
    mock_client_class.return_value = mock_client
    
    publisher = MQTTPublisher(mqtt_config)
    
    # Verify client setup
    mock_client_class.assert_called_once()
    mock_client.username_pw_set.assert_called_once_with("testuser", "testpass")
    mock_client.tls_set_context.assert_called_once()
    
    # Verify callbacks are set
    assert publisher.client.on_connect == publisher._on_connect
    assert publisher.client.on_disconnect == publisher._on_disconnect
    assert publisher.client.on_publish == publisher._on_publish


@patch('src.mqtt_client.mqtt.Client')
def test_mqtt_publisher_connect_success(mock_client_class, mqtt_config):
    """Test successful MQTT connection."""
    mock_client = Mock()
    mock_client_class.return_value = mock_client
    mock_client.connect.return_value = None
    
    publisher = MQTTPublisher(mqtt_config)
    result = publisher.connect()
    
    assert result is True
    mock_client.connect.assert_called_once_with("test.broker.com", 1883, 60)


@patch('src.mqtt_client.mqtt.Client')
def test_mqtt_publisher_connect_failure(mock_client_class, mqtt_config):
    """Test MQTT connection failure."""
    mock_client = Mock()
    mock_client_class.return_value = mock_client
    mock_client.connect.side_effect = Exception("Connection failed")
    
    publisher = MQTTPublisher(mqtt_config)
    result = publisher.connect()
    
    assert result is False


@patch('src.mqtt_client.mqtt.Client')
def test_mqtt_publisher_publish_success(mock_client_class, mqtt_config):
    """Test successful message publishing."""
    mock_client = Mock()
    mock_client_class.return_value = mock_client
    
    # Mock successful publish
    mock_result = Mock()
    mock_result.rc = 0  # MQTT_ERR_SUCCESS
    mock_client.publish.return_value = mock_result
    
    publisher = MQTTPublisher(mqtt_config)
    result = publisher.publish("test/topic", "test payload")
    
    assert result is True
    mock_client.publish.assert_called_once_with("test/topic", "test payload", qos=1)


@patch('src.mqtt_client.mqtt.Client')
def test_mqtt_publisher_context_manager(mock_client_class, mqtt_config):
    """Test MQTT publisher as context manager."""
    mock_client = Mock()
    mock_client_class.return_value = mock_client
    mock_client.connect.return_value = None
    
    publisher = MQTTPublisher(mqtt_config)
    
    with publisher as pub:
        assert pub is publisher
        mock_client.connect.assert_called_once()
    
    mock_client.disconnect.assert_called_once()


def test_mqtt_config_defaults():
    """Test MQTT configuration defaults."""
    config = MQTTConfig(
        server="broker.local",
        username="user",
        password="pass"
    )
    
    assert config.port == 1883
    assert config.use_tls is True
    assert config.client_id is None
