# Your Rasa version
RASA_VERSION := 3.13.7

#####
# Utility targets for help and variable inspection
ECHO := @echo

.PHONY: help $(shell grep -E '^[a-zA-Z_-]+:' $(MAKEFILE_LIST) | sed 's/://')
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-variables: ## Print all Makefile variables
	$(ECHO) "Makefile Variables:"
	$(ECHO) "RASA_VERSION: $(RASA_VERSION)"
	$(ECHO) "RASA_PRO_LICENSE: $(RASA_PRO_LICENSE)"
	$(ECHO) "OPENAI_API_KEY: $(OPENAI_API_KEY)"

#####
# Remove Rasa model, and log files, and clean up Python cache files
clean:
	$(ECHO) "Cleaning files..."
	rm -rf .rasa/* models/* logs/*
	find . -name '*.py[co]' -o -name '*~' -exec rm -f {} +

# Windows
ifeq ($(OS), Windows_NT)
  SHELL := powershell.exe
  .SHELLFLAGS := -NoProfile -Command
  define RASA_DOCKER_MODEL
    docker run --rm -v "$${PWD}:/app" \
      -e RASA_PRO_LICENSE=$$env:RASA_PRO_LICENSE \
      -e OPENAI_API_KEY=$$env:OPENAI_API_KEY \
      rasa/rasa-pro:$(RASA_VERSION) $(1)
  endef
  define RASA_DOCKER
    docker run -v "$${PWD}:/app" -p 5005:5005 \
      -e RASA_PRO_LICENSE=$$env:RASA_PRO_LICENSE \
      -e OPENAI_API_KEY=$$env:OPENAI_API_KEY \
      rasa/rasa-pro:$(RASA_VERSION) $(1)
  endef
# MacOS and Linux
else
  SHELL := /bin/bash
  .SHELLFLAGS := -eu -o pipefail -c
  define RASA_DOCKER_MODEL
    docker run --rm -v "$$PWD:/app" \
      -e RASA_PRO_LICENSE="$$RASA_PRO_LICENSE" \
      -e OPENAI_API_KEY="$$OPENAI_API_KEY" \
      rasa/rasa-pro:$(RASA_VERSION) $(1)
  endef
  define RASA_DOCKER
    docker run -v "$$PWD:/app" -p 5005:5005 \
      -e RASA_PRO_LICENSE="$$RASA_PRO_LICENSE" \
      -e OPENAI_API_KEY="$$OPENAI_API_KEY" \
      rasa/rasa-pro:$(RASA_VERSION) $(1)
  endef
endif

# Train and validate the Rasa model
model:
	$(ECHO) "Training Rasa model..."
	$(call RASA_DOCKER_MODEL, train)

# Start Rasa Inspector with logging enabled
inspect:
	$(ECHO) "Starting Rasa Inspector with logging..."
	mkdir -p logs/
	$(call RASA_DOCKER, inspect --debug --log-file logs/logs.out)

# Start the Rasa server with logging enabled
run:
	$(ECHO) "Starting Rasa Server with logging..."
	mkdir -p logs/
	$(call RASA_DOCKER, run --debug --log-file logs/logs.out --enable-api --cors "*")

# Run end-to-end tests on the Rasa model
test:
	$(ECHO) "Testing Rasa model..."
	$(call RASA_DOCKER, test e2e tests/)
