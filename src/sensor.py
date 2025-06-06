"""Temperature and humidity sensor interface."""

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Tuple

import structlog

logger = structlog.get_logger(__name__)


@dataclass
class SensorReading:
    """Sensor reading data."""

    temperature: float
    humidity: float
    timestamp: float

    @property
    def temperature_f(self) -> float:
        """Temperature in Fahrenheit."""
        return self.temperature * 9.0 / 5.0 + 32.0


class SensorInterface(ABC):
    """Abstract interface for temperature/humidity sensors."""

    @abstractmethod
    def read(self) -> Optional[SensorReading]:
        """Read temperature and humidity from sensor."""
        pass


class DHT22Sensor(SensorInterface):
    """DHT22 temperature and humidity sensor."""

    def __init__(self, pin: int, max_retries: int = 3) -> None:
        self.pin = pin
        self.max_retries = max_retries

        # Import DHT library (only available on Pi)
        try:
            import Adafruit_DHT as dht

            self.dht = dht
            self.sensor_type = dht.DHT22
            logger.info("DHT22 sensor initialized", pin=pin)
        except ImportError:
            logger.warning("Adafruit_DHT not available, using mock sensor")
            self.dht = None
            self.sensor_type = None

    def read(self) -> Optional[SensorReading]:
        """Read temperature and humidity from DHT22 sensor."""
        if self.dht is None:
            # Return mock data for development
            return SensorReading(temperature=22.5, humidity=45.0, timestamp=time.time())

        for attempt in range(self.max_retries):
            try:
                humidity, temperature = self.dht.read_retry(self.sensor_type, self.pin)

                if humidity is not None and temperature is not None:
                    logger.info(
                        "Sensor reading successful",
                        temperature=temperature,
                        humidity=humidity,
                        attempt=attempt + 1,
                    )

                    return SensorReading(
                        temperature=temperature,
                        humidity=humidity,
                        timestamp=time.time(),
                    )
                else:
                    logger.warning("Sensor returned None values", attempt=attempt + 1)

            except Exception as e:
                logger.error("Sensor read error", attempt=attempt + 1, error=str(e))

            if attempt < self.max_retries - 1:
                time.sleep(1)  # Wait before retry

        logger.error(
            "Failed to read sensor after all retries",
            max_retries=self.max_retries,
        )
        return None


class MockSensor(SensorInterface):
    """Mock sensor for testing."""

    def __init__(self, temperature: float = 22.0, humidity: float = 50.0) -> None:
        self.temperature = temperature
        self.humidity = humidity

    def read(self) -> Optional[SensorReading]:
        """Return mock sensor reading."""
        return SensorReading(
            temperature=self.temperature,
            humidity=self.humidity,
            timestamp=time.time(),
        )
