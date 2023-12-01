.DEFAULT_GOAL := help

VENV :=.venv

.PHONY: install
install:  ## Install a virtual environment
	python -m venv ${VENV}
	${VENV}/bin/pip install --upgrade pip
	${VENV}/bin/pip install -r requirements.txt

.PHONY: clean
clean:  ## Clean up caches and build artifacts
	@git clean -X -d -f

.PHONY: help
help:  ## Display this help screen
	@echo -e "\033[1mAvailable commands:\033[0m"
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' | sort

.PHONY: jupyter
jupyter: install ## Start jupyterlab
	${VENV}/bin/pip install jupyterlab
	${VENV}/bin/jupyter lab
