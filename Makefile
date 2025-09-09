# Makefile for Django Docker Compose Project

# Variables
DOCKER_COMPOSE := docker compose

# Targets
.PHONY: build up down logs shell migrate test

build: ## Build all Docker images
	$(DOCKER_COMPOSE) build

up: ## Start the services in detached mode
	$(DOCKER_COMPOSE) -f compose-dev.yaml up -d --build

up-prod: ## Start the services in detached mode
	$(DOCKER_COMPOSE) -f compose-prod.yaml up -d --build

down: ## Stop and remove the services
	$(DOCKER_COMPOSE) down

logs: ## View the logs of the services
	$(DOCKER_COMPOSE) logs -f

shell: ## Open a shell in the Django web service container
	$(DOCKER_COMPOSE) exec web bash

migrate: ## Run Django migrations
	$(DOCKER_COMPOSE) exec web python manage.py migrate

test: ## Run Django tests
	$(DOCKER_COMPOSE) exec web python manage.py test

# Helper target to list available commands with descriptions
.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
