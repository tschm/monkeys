.DEFAULT_GOAL := help

SHELL=/bin/bash

UNAME=$(shell uname -s)


.PHONY: install
install:  ## Install a virtual environment
	@poetry install -vv


.PHONY: clean
clean:  ## Clean up caches and build artifacts
	@git clean -X -d -f


.PHONY: help
help:  ## Display this help screen
	@echo -e "\033[1mAvailable commands:\033[0m"
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' | sort


.PHONY: jupyter
jupyter: install ## Run jupyter lab
	@poetry run pip install jupyterlab
	@poetry run jupyter lab


.PHONY: marimo
marimo: install ## Run jupyter lab
	@poetry run pip install marimo
	@poetry run marimo edit

