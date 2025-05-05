#################################################################################
#
# Makefile to build the project and run checks
#
#################################################################################

PROJECT_NAME = Data-Streaming-Project
REGION = eu-west-2
PYTHON_INTERPRETER = python
WD = $(shell pwd)
PYTHONPATH = $(WD)
SHELL := /bin/bash
PROFILE = default
PIP := pip

## Create python interpreter environment.
create-environment:
	@echo ">>> About to create environment: $(PROJECT_NAME)..."
	@echo ">>> Checking Python version"
	( \
		$(PYTHON_INTERPRETER) --version; \
	)
	@echo ">>> Setting up VirtualEnv."
	( \
	    $(PIP) install -q virtualenv virtualenvwrapper; \
	    virtualenv venv --python=$(PYTHON_INTERPRETER); \
	)

# Define utility variable to help calling Python from the virtual environment
ACTIVATE_ENV := source venv/bin/activate

# Execute Python-related commands from within the environment
define execute_in_env
	$(ACTIVATE_ENV) && $1
endef

## Build the environment requirements
requirements: create-environment
	$(call execute_in_env, $(PIP) install -r ./requirements.txt)

################################################################################################################
# Setup Dev Tools

## Install bandit
bandit:
	$(call execute_in_env, $(PIP) install bandit)

## Install safety
safety:
	$(call execute_in_env, $(PIP) install safety)

## Install pip-audit
pip-audit:
	$(call execute_in_env, $(PIP) install pip-audit)

## Install black
black:
	$(call execute_in_env, $(PIP) install black)

## Install checkov (Terraform security)
checkov:
	$(call execute_in_env, $(PIP) install checkov)

## Set up dev requirements (bandit, safety, pip-audit, black, checkov)
dev-setup: bandit safety pip-audit black checkov coverage

################################################################################################################
# Tests and Checks

## Run security checks
security-test:
	$(call execute_in_env, safety check -r ./requirements.txt)
	$(call execute_in_env, pip-audit -r ./requirements.txt)
	$(call execute_in_env, bandit -lll -r ./src)

## Format code using black
run-black:
	$(call execute_in_env, black ./src ./test)

## Run unit tests
unit-tests:
	$(call execute_in_env, PYTHONPATH=$(PYTHONPATH) pytest --vvvrP)

## Check Terraform/IaC code for security issues
iac-check:
	$(call execute_in_env, checkov -d ./infra)

## Run all checks
run-checks: security-test run-black unit-tests iac-check

################################################################################################################
# Lambda Layer Packaging

## Clean and create requests layer zip
build-requests-layer:
	@echo ">>> Creating requests Lambda layer..."
	rm -rf layer_build && \
	mkdir -p layer_build/python && \
	$(PIP) install requests -t layer_build/python && \
	cd layer_build && zip -r ../requests_layer.zip python && \
	cd .. && rm -rf layer_build
	@echo ">>> requests_layer.zip created successfully."