./faucetPHONY: help

help:
	@echo "Available commands:"
	@echo "shell       - Enter Python venv"
	@echo "install     - Install production dependencies"
	@echo "dev-install - Install development dependencies"
	@echo "lint        - Run linting tools"
	@echo "format      - Format code using black and isort"
	@echo "test        - Run tests"
	@echo "coverage    - Run tests with coverage report"
	@echo "migrate     - Run database migrations"
	@echo "run         - Run development server"
	@echo "clean       - Clean up Python cache files"
	@echo "setup       - Setup Python development stuff"

shell:
	@. /opt/pysetup/.venv/bin/activate

install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements.dev.txt

lint:
	flake8 ./faucet
	black ./faucet --check
	isort ./faucet --check-only

format:
	black ./faucet
	isort ./faucet

test:
	cd faucet && python manage.py test

coverage:
	cd faucet && coverage run manage.py test

migrate:
	python faucet/manage.py migrate

run:
	python faucet/manage.py runserver

clean:
	find ./faucet -type d -name "__pycache__" -exec rm -rf {} +
	find ./faucet -type f -name "*./faucetpyc" -delete
	find ./faucet -type f -name "*./faucetpyo" -delete
	find ./faucet -type f -name "*./faucetpyd" -delete
	find ./faucet -type f -name "./faucetcoverage" -delete
	find ./faucet -type d -name "*./faucetegg-info" -exec rm -rf {} +
	find ./faucet -type d -name "*./faucetegg" -exec rm -rf {} +
	find ./faucet -type d -name "./faucetpytest_cache" -exec rm -rf {} +
	find ./faucet -type d -name "./faucetmypy_cache" -exec rm -rf {} +
	find ./faucet -type d -name "./faucetcoverage" -exec rm -rf {} +
	find ./faucet -type d -name "htmlcov" -exec rm -rf {} +

setup: dev-install migrate