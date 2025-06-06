# Development Scripts

## Local Development
```powershell
# Install development dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install

# Run tests
python -m pytest

# Run with coverage
python -m pytest --cov=src --cov-report=html

# Format code
black src/ tests/
isort src/ tests/

# Type checking
mypy src/

# Run locally (make sure to copy .env.example to .env first)
python -m src.main
```

## Docker Development
```powershell
# Build image
docker build -t temperature-sensor .

# Run with docker-compose (includes MQTT broker for testing)
docker-compose --profile testing up

# Run just the sensor
docker-compose up temperature-sensor
```

## Raspberry Pi Deployment

### Option 1: Direct Python Installation
```bash
# On the Pi
git clone <your-repo> /opt/temperature-sensor
cd /opt/temperature-sensor
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings

# Run as service
sudo cp systemd/temperature-sensor.service /etc/systemd/system/
sudo systemctl enable temperature-sensor
sudo systemctl start temperature-sensor
```

### Option 2: Docker Deployment
```bash
# On the Pi
git clone <your-repo> /opt/temperature-sensor
cd /opt/temperature-sensor
cp .env.example .env
# Edit .env with your settings

# Build and run
docker-compose up -d
```

### Option 3: Ansible Deployment (Recommended)
```powershell
# From your development machine
cd ansible

# Edit inventory.ini with your Pi IPs
# Create vault file for secrets
ansible-vault create secrets.yml

# Deploy to all Pis
ansible-playbook -i inventory.ini deploy.yml --ask-vault-pass

# Deploy to specific Pi
ansible-playbook -i inventory.ini deploy.yml --limit raspberrypi-0w1 --ask-vault-pass
```

## Monitoring and Logs
```bash
# View service status
sudo systemctl status temperature-sensor

# View logs
sudo journalctl -u temperature-sensor -f

# Docker logs
docker-compose logs -f temperature-sensor
```
