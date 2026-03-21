
APP_DIR = src
VENV_BIN = b_s_env/bin/

.PHONY: help update-code docker-up docker-down docker-rebuild lint format check-all venv-install

help:
	@echo "  make update      
	@echo "  make up          
	@echo "  make down        
	@echo "  make lint        
	@echo "  make format      
	@echo "  make check       

editor:
	code .

update:
	@echo "Git Pulling..."
	git pull origin main
	@echo "Docker restarting..."
	docker compose down
	docker compose up -d --build
	@echo "Updating finished!"

up:
	docker compose up -d

down:
	docker compose down

rebuild:
	docker compose up -d --build


format:
	@echo "Formatting code..."
	$(VENV_BIN)ruff format .
	$(VENV_BIN)ruff check . --fix

lint:
	@echo "Checking styles and formats..."
	$(VENV_BIN)ruff check .
	$(VENV_BIN)mypy .

check: format lint
	@echo "Format lint revision completed"


install:
	python3 -m venv venv
	venv/bin/pip install -r requirements.txt

start: editor update install check rebuild

