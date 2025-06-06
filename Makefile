# Temperature Sensor Project Makefile

.PHONY: help install test lint format clean docker-build docker-run deploy-ansible

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install development dependencies
	pip install -r requirements-dev.txt
	pre-commit install

test: ## Run tests
	python -m pytest -v

test-cov: ## Run tests with coverage
	python -m pytest --cov=src --cov-report=html --cov-report=term

lint: ## Run linting checks
	black --check src/ tests/
	isort --check-only src/ tests/
	flake8 src/ tests/
	mypy src/

format: ## Format code
	black src/ tests/
	isort src/ tests/

clean: ## Clean build artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage

docker-build: ## Build Docker image
	docker build -t temperature-sensor .

docker-run: ## Run with Docker Compose
	docker-compose up --build

docker-test: ## Run with test MQTT broker
	docker-compose --profile testing up --build

deploy-ansible: ## Deploy with Ansible (requires vault password)
	cd ansible && ansible-playbook -i inventory.ini deploy.yml --ask-vault-pass

dev-setup: ## Complete development setup
	@echo "Setting up development environment..."
	cp .env.example .env
	@echo "Please edit .env file with your MQTT broker settings"
	make install
	@echo "Development setup complete!"

pi-install: ## Install directly on Raspberry Pi
	sudo apt update
	sudo apt install -y python3 python3-pip python3-venv git
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt
	cp .env.example .env
	@echo "Please edit .env file and run: ./venv/bin/python -m src.main"
