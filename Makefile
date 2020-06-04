TARGET_USERNAME?=golemproject
LOCAL_PATH?=$(shell pwd)
CONTAINER_PATH?=/output

check_defined = \
    $(strip $(foreach 1,$1, \
        $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
        $(error Undefined $1$(if $2, ($2))$(if $(value @), \
                required by target `$@')))

.PHONY: install
install: ## Install requirements
	python -m pip install -r requirements.txt

.PHONY: clean-pyc
clean-pyc: ## Remove python artifacts
	find tweetbrief/ -name "__pycache__" -exec rm --force --recursive {} +
	find tweetbrief/ -name "*.pyc" -exec rm --force {} +
	find tweetbrief/ -name "*.pyo" -exec rm --force {} +
	find tweetbrief/ -name "*~" -exec rm --force {} +

.PHONY: clean-build
clean-build: ## Remove build artifact
	rm --force --recursive tweetbrief/build/
	rm --force --recursive tweetbrief/dist/
	rm --force --recursive tweetbrief/*.egg-info

.PHONY: isort
isort: ## Sort import statements
	python -m pip install isort==4.3.21
	python -m isort --skip-glob=.tox --recursive tweetbrief/

.PHONY: black
black: ## Check style with black
	python -m pip install black==19.10b0
	python -m black --line-length=119 --exclude=.tox tweetbrief/

.PHONY: run
run: ## Run the `tweetbrief` service on the local machine
	@:$(call check_defined, CONSUMER_KEY)
	@:$(call check_defined, CONSUMER_SECRET)
	python tweetbrief/runner.py

.PHONY: docker-run
docker-run: ## Build and run the `tweetbrief` service in a Docker container
	docker build \
		--file=Dockerfile \
		--tag=wildland/tweetbrief .
	docker run \
		--detach=false
		--name=tweetbrief
		--env-file=.env
		--env=TARGET_USERNAME=$(TARGET_USERNAME)
		--volume=$(LOCAL_PATH):$(CONTAINER_PATH)	

.DEFAULT_GOAL: help
.PHONY: help
help:
	@awk -F ':|##' '/^[^\t].+?:.*?##/ {\
    printf "\033[36m%-30s\033[0m %s\n", $$1, $$NF \
    }' $(MAKEFILE_LIST)
