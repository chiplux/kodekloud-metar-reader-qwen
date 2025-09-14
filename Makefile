# Makefile for METAR Reader Application

# Variables
IMAGE_NAME = metar-reader
CONTAINER_NAME = metar-reader-app
PORT = 5000

# Default target
.PHONY: help
help:
	@echo "METAR Reader - Makefile Commands"
	@echo "================================"
	@echo "build      - Build the Docker image (production)"
	@echo "build-dev  - Build the Docker image (development)"
	@echo "run        - Run the application in a container (production)"
	@echo "run-dev    - Run the application in a container (development)"
	@echo "dev        - Run the application in development mode with live reload"
	@echo "stop       - Stop the running container"
	@echo "test       - Run unit tests"
	@echo "test-dev   - Run unit tests in development container"
	@echo "clean      - Remove the Docker image"
	@echo "logs       - View container logs"
	@echo "shell      - Access the container shell"
	@echo "deploy     - Build and deploy the application"
	@echo "size       - Show Docker image sizes"
	@echo "help       - Show this help message"

# Build the Docker image (production)
.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

# Build the Docker image (development)
.PHONY: build-dev
build-dev:
	docker build -t $(IMAGE_NAME)-dev -f Dockerfile.dev .

# Run the application in a container (production)
.PHONY: run
run: build
	docker run -d --name $(CONTAINER_NAME) -p $(PORT):5000 $(IMAGE_NAME)

# Run the application in a container (development)
.PHONY: run-dev
run-dev: build-dev
	docker run -d --name $(CONTAINER_NAME) -p $(PORT):5000 -v $(PWD):/app $(IMAGE_NAME)-dev

# Run the application in development mode (with live reload)
.PHONY: dev
dev: build-dev
	docker run -d --name $(CONTAINER_NAME) -p $(PORT):5000 -v $(PWD):/app $(IMAGE_NAME)-dev

# Stop the running container
.PHONY: stop
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# Run unit tests (production image)
.PHONY: test
test: build
	docker run --rm $(IMAGE_NAME) python -m pytest tests/ -v

# Run unit tests (development image)
.PHONY: test-dev
test-dev: build-dev
	docker run --rm $(IMAGE_NAME)-dev python -m pytest tests/ -v

# Remove the Docker image
.PHONY: clean
clean:
	docker rmi $(IMAGE_NAME) || true
	docker rmi $(IMAGE_NAME)-dev || true

# View container logs
.PHONY: logs
logs:
	docker logs -f $(CONTAINER_NAME)

# Access the container shell
.PHONY: shell
shell: build
	docker run -it --rm $(IMAGE_NAME) /bin/sh

# Access the development container shell
.PHONY: shell-dev
shell-dev: build-dev
	docker run -it --rm $(IMAGE_NAME)-dev /bin/sh

# Build and deploy the application
.PHONY: deploy
deploy: stop build run
	@echo "Application deployed successfully!"
	@echo "Access it at http://localhost:$(PORT)"

# Show Docker image sizes
.PHONY: size
size:
	@echo "Docker Image Sizes:"
	@docker images $(IMAGE_NAME)* --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# Install dependencies locally (for development)
.PHONY: install
install:
	pip install -r requirements-dev.txt

# Run the application locally (for development)
.PHONY: run-local
run-local:
	python app.py