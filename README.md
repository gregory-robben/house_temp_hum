# Temperature & Humidity Sensor for Home Assistant

A modern, containerized Python application for reading DHT22 temperature and humidity sensors on Raspberry Pi and publishing the data to Home Assistant via MQTT.

## Features

- 🏠 **Home Assistant Integration**: Direct MQTT publishing with proper discovery
- 🐳 **Container Ready**: Docker support with GPIO access on Raspberry Pi
- 🔧 **Development Container**: Full VS Code dev container setup for remote development
- 🚀 **Ansible Deployment**: Automated provisioning and deployment
- 🔒 **Secure**: Proper credential management and TLS support
- 📊 **Monitoring**: Structured logging and health checks
- 🧪 **Tested**: Comprehensive test suite with mocking for development

## Quick Start

### Development Setup

1. **Clone and open in VS Code**:
   ```bash
   git clone <your-repo>
   code house_temp_hum
   ```

2. **Reopen in Dev Container**: VS Code will prompt to reopen in container

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your MQTT broker details
   ```

4. **Run locally**:
   ```bash
   python -m src.main
   ```

### Production Deployment

#### Option 1: Ansible (Recommended)
```bash
cd ansible
# Edit inventory.ini with your Pi details
ansible-vault create secrets.yml  # Add MQTT credentials
ansible-playbook -i inventory.ini deploy.yml --ask-vault-pass
```

#### Option 2: Docker on Pi
```bash
# On your Raspberry Pi
git clone <your-repo> /opt/temperature-sensor
cd /opt/temperature-sensor
cp .env.example .env
# Edit .env file
docker-compose up -d
```

## Configuration

The application uses environment variables for configuration:

| Variable | Description | Default |
|----------|-------------|---------|
| `MQTT_SERVER` | MQTT broker hostname | - |
| `MQTT_USERNAME` | MQTT username | - |
| `MQTT_PASSWORD` | MQTT password | - |
| `MQTT_USE_TLS` | Enable TLS encryption | `true` |
| `SENSOR_PIN` | GPIO pin for DHT22 | `4` |
| `SENSOR_READ_INTERVAL` | Seconds between readings | `300` |
| `SENSOR_METRIC_UNITS` | Use Celsius vs Fahrenheit | `true` |

## Device Mapping

The application automatically detects the hostname and maps to location:

- `raspberrypi-0w1` → Office
- `raspberrypi-0w2` → Bedroom  
- `raspberrypi-0w3` → Plant area
- `raspberrypi-0w4` → Dining room

## Architecture

```
src/
├── config.py          # Configuration management with Pydantic
├── sensor.py          # DHT22 sensor interface with retry logic
├── mqtt_client.py     # MQTT client with TLS and authentication  
└── main.py           # Main application with structured logging
```

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed development instructions.

## Migration from Legacy Version

The legacy `tempsensor.py` is replaced by the new modular structure. Key improvements:

- ✅ **Type Safety**: Full type hints with mypy checking
- ✅ **Error Handling**: Proper exception handling and retries
- ✅ **Logging**: Structured JSON logging instead of print statements
- ✅ **Testing**: Comprehensive test suite with >90% coverage
- ✅ **Security**: Environment-based secrets management
- ✅ **Monitoring**: Health checks and service status monitoring

## License

MIT License - see [LICENSE](LICENSE) file.
