SHELL := /bin/sh
include .env
export $(shell sed 's/=.*//' .env)
export TARGET_USERNAME ?= golemproject
export HOST_OUTPUT = ./briefs

run: export BRIEF_OUTPUT ?= ./briefs
docker-run: export BRIEF_OUTPUT ?= /output

check_defined = \
    $(strip $(foreach 1,$1, \
        $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
        $(error Undefined $1$(if $2, ($2))$(if $(value @), \
                required by target `$@')))

.PHONY: install
install: ## Install requirements
	pipenv install

.PHONY: install-dev
install-dev: ## Install dev requirements
	pipenv install --dev

.PHONY: clean-pyc
clean-pyc: ## Remove python artifacts
	find tweetbrief/ -name "__pycache__" -exec rm -rf {} +
	find tweetbrief/ -name "*.pyc" -exec rm -f {} +
	find tweetbrief/ -name "*.pyo" -exec rm -f {} +
	find tweetbrief/ -name "*~" -exec rm -f {} +

.PHONY: clean-build
clean-build: ## Remove build artifact
	rm -rf tweetbrief/build/
	rm -rf tweetbrief/dist/
	rm -rf tweetbrief/*.egg-info

.PHONY: isort
isort: ## Sort import statements
	pipenv run python -m isort --skip-glob=.tox --recursive tweetbrief/

.PHONY: black
black: ## Check style with black
	pipenv run python -m black --line-length=119 --exclude=.tox tweetbrief/

.PHONY: run
run: prerun ## Run the `tweetbrief` service on the local machine
	pipenv run python tweetbrief/runner.py

.PHONY: docker-run
docker-run: prerun ## Build and run the `tweetbrief` service in a Docker container
	docker-compose up --build

.DEFAULT_GOAL := help
.PHONY: help
help:
	@awk -F ':|##' '/^[^\t].+?:.*?##/ {\
    printf "\033[36m%-30s\033[0m %s\n", $$1, $$NF \
    }' $(MAKEFILE_LIST)

.PHONY: prerun
prerun:
	@:$(call check_defined, CONSUMER_KEY)
	@:$(call check_defined, CONSUMER_SECRET)
