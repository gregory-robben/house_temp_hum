"""Main temperature sensor application."""

import signal
import sys
import time

import structlog

from .config import get_config
from .mqtt_client import MQTTPublisher
from .sensor import DHT22Sensor, SensorReading

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="ISO"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)


class TemperatureSensorApp:
    """Main temperature sensor application."""

    def __init__(self) -> None:
        self.config = get_config()
        self.sensor = DHT22Sensor(
            pin=self.config.sensor.pin,
            max_retries=self.config.sensor.max_retries,
        )
        self.mqtt_client = MQTTPublisher(self.config.mqtt)
        self.running = True

        # Set up signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        logger.info(
            "Temperature sensor app initialized",
            hostname=self.config.hostname,
            location=self.config.current_device.location,
        )

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info("Received shutdown signal", signal=signum)
        self.running = False

    def _publish_reading(self, reading: SensorReading) -> bool:
        """Publish sensor reading to MQTT."""
        device = self.config.current_device

        # Format values
        if self.config.sensor.metric_units:
            temp_value = f"{reading.temperature:.2f}"
        else:
            temp_value = f"{reading.temperature_f:.2f}"

        humidity_value = f"{reading.humidity:.2f}"

        # Publish temperature
        temp_success = self.mqtt_client.publish(device.mqtt_temp_topic, temp_value)

        # Publish humidity
        humidity_success = self.mqtt_client.publish(
            device.mqtt_humid_topic, humidity_value
        )

        return temp_success and humidity_success

    def run_once(self) -> bool:
        """Run one sensor reading cycle."""
        reading = self.sensor.read()
        if reading is None:
            logger.error("Failed to get sensor reading")
            return False

        logger.info(
            "Sensor reading obtained",
            temperature=reading.temperature,
            humidity=reading.humidity,
        )

        try:
            with self.mqtt_client:
                return self._publish_reading(reading)
        except Exception as e:
            logger.error("Failed to publish reading", error=str(e))
            return False

    def run_continuous(self) -> None:
        """Run continuous sensor monitoring."""
        logger.info(
            "Starting continuous monitoring",
            interval=self.config.sensor.read_interval,
        )

        while self.running:
            try:
                success = self.run_once()
                if not success:
                    logger.warning("Sensor reading cycle failed")

                # Wait for next reading
                time.sleep(self.config.sensor.read_interval)

            except Exception as e:
                logger.error("Unexpected error in main loop", error=str(e))
                time.sleep(5)  # Brief pause before retry

        logger.info("Temperature sensor app stopped")


def main() -> None:
    """Main entry point."""
    try:
        app = TemperatureSensorApp()
        app.run_continuous()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error("Application failed", error=str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
