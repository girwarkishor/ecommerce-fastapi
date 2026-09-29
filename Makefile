install:
	# Install dependencies
	uv sync
lint:
	# Run linters
	ruff check . --fix
format:
	# Format code
	black .
test:
	# Run tests
deploy:
	# Deploy the application
