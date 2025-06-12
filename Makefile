# Colors for pretty output
BLUE := \033[36m
BOLD := \033[1m
RESET := \033[0m

.DEFAULT_GOAL := help

.PHONY: help fmt demo download clean uv marimo

##@ Development Setup

uv: ##! Install uv package manager
	@printf "$(BLUE)Installing uv (and uvx)...$(RESET)\n"
	@curl -LsSf https://astral.sh/uv/install.sh | sh

##@ Code Quality

fmt: uv ## Run code formatting and linting
	@printf "$(BLUE)Running formatters and linters...$(RESET)\n"
	@uvx pre-commit install
	@uvx pre-commit run --all-files

##@ Marimo Notebooks

marimo: uv ##! Start a Marimo server with specified notebook (usage: make marimo NOTEBOOK=filename.py)
	@printf "$(BLUE)Starting Marimo server for $(NOTEBOOK)...$(RESET)\n"
	@uvx marimo edit --sandbox book/marimo/$(NOTEBOOK)

demo: ## Run the monkey portfolio simulation notebook
	@$(MAKE) marimo NOTEBOOK=monkey.py

download: ## Run the price download notebook
	@$(MAKE) marimo NOTEBOOK=download_prices.py

##@ Cleanup

clean: ## Clean generated files and directories
	@printf "$(BLUE)Cleaning project...$(RESET)\n"
	@git clean -d -X -f

##@ Help

help:  ## Show this help message
	@printf "$(BOLD)Usage:$(RESET)\n  make $(BLUE)<target>$(RESET)\n\n"
	@printf "$(BOLD)Targets:$(RESET)\n"
	@awk 'BEGIN {FS = ":.*##"; OFS = ""} \
		/^##@/ { printf "\n$(BOLD)%s$(RESET)\n", substr($$0, 5); next } \
		/^[a-zA-Z0-9_-]+:.*##[^!]/ { printf "  $(BLUE)%-15s$(RESET) %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
