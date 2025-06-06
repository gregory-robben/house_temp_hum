"""Configuration management for temperature sensor."""
import socket
from pathlib import Path
from typing import Dict, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DeviceConfig(BaseSettings):
    """Device-specific configuration."""
    
    location: str
    mqtt_temp_topic: str
    mqtt_humid_topic: str


class MQTTConfig(BaseSettings):
    """MQTT configuration."""
    
    model_config = SettingsConfigDict(env_prefix="MQTT_")
    
    server: str = Field(..., description="MQTT broker hostname or IP")
    port: int = Field(default=1883, description="MQTT broker port")
    username: str = Field(..., description="MQTT username")
    password: str = Field(..., description="MQTT password")
    use_tls: bool = Field(default=True, description="Use TLS encryption")
    client_id: Optional[str] = Field(default=None, description="MQTT client ID")


class SensorConfig(BaseSettings):
    """Sensor configuration."""
    
    model_config = SettingsConfigDict(env_prefix="SENSOR_")
    
    pin: int = Field(default=4, description="GPIO pin for DHT sensor")
    read_interval: int = Field(default=300, description="Seconds between readings")
    metric_units: bool = Field(default=True, description="Use metric units")
    max_retries: int = Field(default=3, description="Max retries for sensor reads")


class AppConfig(BaseSettings):
    """Main application configuration."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # Device mapping
    devices: Dict[str, DeviceConfig] = {
        "raspberrypi-0w1": DeviceConfig(
            location="office",
            mqtt_temp_topic="homeassistant/sensor/office/temperature",
            mqtt_humid_topic="homeassistant/sensor/office/humidity",
        ),
        "raspberrypi-0w2": DeviceConfig(
            location="bedroom",
            mqtt_temp_topic="homeassistant/sensor/bedroom/temperature",
            mqtt_humid_topic="homeassistant/sensor/bedroom/humidity",
        ),
        "raspberrypi-0w3": DeviceConfig(
            location="plant",
            mqtt_temp_topic="homeassistant/sensor/plant/temperature",
            mqtt_humid_topic="homeassistant/sensor/plant/humidity",
        ),
        "raspberrypi-0w4": DeviceConfig(
            location="dining",
            mqtt_temp_topic="homeassistant/sensor/dining/temperature",
            mqtt_humid_topic="homeassistant/sensor/dining/humidity",
        ),
    }
    
    # Component configs
    mqtt: MQTTConfig = Field(default_factory=MQTTConfig)
    sensor: SensorConfig = Field(default_factory=SensorConfig)
    
    @property
    def hostname(self) -> str:
        """Get current hostname."""
        return socket.gethostname()
    
    @property
    def current_device(self) -> DeviceConfig:
        """Get configuration for current device."""
        if self.hostname not in self.devices:
            raise ValueError(f"Unknown hostname: {self.hostname}")
        return self.devices[self.hostname]


def get_config() -> AppConfig:
    """Get application configuration."""
    return AppConfig()
