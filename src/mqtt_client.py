"""MQTT client for publishing sensor data."""

import ssl
from typing import Optional

import paho.mqtt.client as mqtt
import structlog

from .config import MQTTConfig

logger = structlog.get_logger(__name__)


class MQTTPublisher:
    """MQTT client for publishing sensor data."""

    def __init__(self, config: MQTTConfig) -> None:
        self.config = config
        self.client = mqtt.Client(
            client_id=config.client_id or f"tempsensor_{config.server}",
            protocol=mqtt.MQTTv311,
        )

        # Set up authentication
        if config.username and config.password:
            self.client.username_pw_set(config.username, config.password)

        # Set up TLS if enabled
        if config.use_tls:
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            self.client.tls_set_context(context)

        # Set up callbacks
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_publish = self._on_publish

    def _on_connect(self, client, userdata, flags, rc):
        """Callback for when client connects."""
        if rc == 0:
            logger.info("Connected to MQTT broker", broker=self.config.server)
        else:
            logger.error(
                "Failed to connect to MQTT broker",
                broker=self.config.server,
                return_code=rc,
            )

    def _on_disconnect(self, client, userdata, rc):
        """Callback for when client disconnects."""
        logger.info("Disconnected from MQTT broker", return_code=rc)

    def _on_publish(self, client, userdata, mid):
        """Callback for when message is published."""
        logger.debug("Message published", message_id=mid)

    def connect(self) -> bool:
        """Connect to MQTT broker."""
        try:
            self.client.connect(self.config.server, self.config.port, 60)
            return True
        except Exception as e:
            logger.error("Failed to connect to MQTT broker", error=str(e))
            return False

    def disconnect(self) -> None:
        """Disconnect from MQTT broker."""
        self.client.disconnect()

    def publish(self, topic: str, payload: str, qos: int = 1) -> bool:
        """Publish message to MQTT topic."""
        try:
            result = self.client.publish(topic, payload, qos=qos)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.info("Published message", topic=topic, payload=payload)
                return True
            else:
                logger.error(
                    "Failed to publish message",
                    topic=topic,
                    payload=payload,
                    return_code=result.rc,
                )
                return False
        except Exception as e:
            logger.error("Error publishing message", topic=topic, error=str(e))
            return False

    def __enter__(self):
        """Context manager entry."""
        if not self.connect():
            raise ConnectionError("Failed to connect to MQTT broker")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
