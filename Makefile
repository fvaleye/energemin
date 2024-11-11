PORT=8000
VERSION=latest

.PHONY: init
init: ## Initialize the project
	$(info --- 🔄 Initialize the project ---)
	uv sync
	@echo "👍"

.PHONY: style
style: ## Style check
	$(info --- 🧹 Style check ---)
	uv tool run ruff check --fix . src
	@echo "👍"

.PHONY: launch-ui
launch-ui: ## Launch the UI
	$(info --- 🤖 Launch the UI ---)
	uv run chainlit run src/app.py --port $(PORT) --host 0.0.0.0
	@echo "👍"

.PHONY: run
run: ## Run the main script
	$(info --- 🚀 Run the main script ---)
	uv run python src/main.py
	@echo "👍"

.PHONY: build
build: ## Build the Docker image
	$(info --- 🐳 Build the Docker image ---)
	docker build --platform linux/amd64 -t energemin-${VERSION} . --build-arg PORT=$(PORT)
	@echo "👍"

.PHONY: test
test: init ## Run the tests
	$(info --- 🧪 Run the tests ---)
	uv run python -m pytest tests
	@echo "👍"

.PHONY: push-to-gcp-artefact
push-to-gcp-artefact: build ## Push the Docker image to GCP Artefact
	$(info --- 📤 Push the Docker image to GCP Artefact ---)
	@if [ -z "${GCP_PROJECT_ID}" ]; then echo "GCP_PROJECT_ID is not set"; exit 1; fi
	@if [ -z "${GCP_LOCATION}" ]; then echo "GCP_LOCATION is not set"; exit 1; fi
	@if [ -z "${REPOSITORY}" ]; then echo "REPOSITORY is not set"; exit 1; fi
	docker tag energemin-${VERSION} ${GCP_LOCATION}-docker.pkg.dev/${GCP_PROJECT_ID}/${REPOSITORY}/energemin:${VERSION}
	docker push ${GCP_LOCATION}-docker.pkg.dev/${GCP_PROJECT_ID}/${REPOSITORY}/energemin:${VERSION}
	@echo "👍"

.PHONY: help
help: ## Show help
	@echo "make init"
	@echo "make run"
	@echo "make style"
	@echo "make launch-ui"
	@echo "make help"