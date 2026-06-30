# Your Rasa version
RASA_VERSION := 3.16.10

# Port used by `make chat` to serve the chat widget
CHAT_PORT := 8000

# Load secrets (RASA_LICENSE, OPENAI_API_KEY) from a local .env if present, then
# export them so they reach the docker `-e` flags below. .env is gitignored.
# Format: plain KEY=value lines (no `export`, no surrounding quotes).
-include .env
# Rasa expects RASA_LICENSE; accept RASA_PRO_LICENSE as an alias if that's what's set.
RASA_LICENSE ?= $(RASA_PRO_LICENSE)
export

#####
# Utility targets for help and variable inspection
ECHO := @echo

# List phony targets
.PHONY: print-variables clean model inspect run chat test help $(HELP_CMDS)

# Help (cross-platform)
HELP_CMDS := help model inspect run chat clean test print-variables
HELP_help    := Show available targets
HELP_model   := Train and validate the Rasa model
HELP_inspect := Inspect the Rasa model (debug/logging)
HELP_run     := Start Rasa server (API enabled)
HELP_chat    := Serve the chat widget and open it in your browser
HELP_clean   := Remove build artifacts
HELP_test    := Run end-to-end tests on the Rasa model
HELP_print-variables := Print all Makefile variables
# Print help text at parse time when `make help` is called
ifeq ($(filter help,$(MAKECMDGOALS)),help)
  $(info Available targets:)
  $(foreach t,$(HELP_CMDS),$(info   $(t) -  $(HELP_$(t))))
endif
help: ; @

print-variables: ## Print all Makefile variables
	$(ECHO) "Makefile Variables:"
	$(ECHO) "RASA_VERSION: $(RASA_VERSION)"
	$(ECHO) "RASA_LICENSE: $(RASA_LICENSE)"
	$(ECHO) "OPENAI_API_KEY: $(OPENAI_API_KEY)"

#####
# OS-specific settings

# Windows
ifeq ($(OS), Windows_NT)
  SHELL := powershell.exe
  .SHELLFLAGS := -NoProfile -Command
  MKDIR_LOG = powershell -NoProfile -Command "New-Item -ItemType Directory -Force logs | Out-Null"
  CLEAN_LOGS = powershell -NoProfile -Command "Remove-Item -Recurse -Force -ErrorAction SilentlyContinue .rasa\*, models\*, logs\*; Get-ChildItem -Recurse -Include *.pyc,*.pyo -Force | Remove-Item -Force -ErrorAction SilentlyContinue; Get-ChildItem -Recurse -Filter '*~' -Force | Remove-Item -Force -ErrorAction SilentlyContinue"
  define RASA_DOCKER_MODEL
    docker run --rm -v "$${PWD}:/app" \
      -e RASA_LICENSE=$$env:RASA_LICENSE \
      -e OPENAI_API_KEY=$$env:OPENAI_API_KEY \
      rasa/rasa-pro:$(RASA_VERSION) $(1)
  endef
  define RASA_DOCKER
    docker run -v "$${PWD}:/app" -p 5005:5005 \
      -e RASA_LICENSE=$$env:RASA_LICENSE \
      -e OPENAI_API_KEY=$$env:OPENAI_API_KEY \
      rasa/rasa-pro:$(RASA_VERSION) $(1)
  endef
  # Serve the chat widget over http and open it in the default browser.
  SERVE_WIDGET = Start-Process "http://localhost:$(CHAT_PORT)"; python -m http.server $(CHAT_PORT) --directory chatwidget
# MacOS and Linux
else
  SHELL := /bin/bash
  .SHELLFLAGS := -eu -o pipefail -c
  MKDIR_LOG = mkdir -p logs
  CLEAN_LOGS = rm -rf .rasa/* models/* logs/* || true; find . -type f \( -name '*.py[co]' -o -name '*~' \) -delete
  define RASA_DOCKER_MODEL
    docker run --rm \
      --user $$(id -u):$$(id -g) \
      -v "$$(pwd):/app" \
      -e RASA_LICENSE="$$RASA_LICENSE" \
      -e OPENAI_API_KEY="$$OPENAI_API_KEY" \
      rasa/rasa-pro:$(RASA_VERSION) $(1)
  endef
  define RASA_DOCKER
    docker run \
      --user $$(id -u):$$(id -g) \
      -v "$$(pwd):/app" \
      -p 5005:5005 \
      -e RASA_LICENSE="$$RASA_LICENSE" \
      -e OPENAI_API_KEY="$$OPENAI_API_KEY" \
      rasa/rasa-pro:$(RASA_VERSION) $(1)
  endef
  # Pick the right "open URL" command: open on macOS, xdg-open on Linux.
  OPEN_URL := $(shell command -v open >/dev/null 2>&1 && echo open || echo xdg-open)
  # Serve the chat widget over http, then open it in the browser once the server is up.
  SERVE_WIDGET = ( sleep 1 && $(OPEN_URL) "http://localhost:$(CHAT_PORT)" ) & python3 -m http.server $(CHAT_PORT) --directory chatwidget
endif

#####
# Remove Rasa model, and log files, and clean up Python cache files
clean:
	$(ECHO) "Cleaning files..."
	$(CLEAN_LOGS)

# Train and validate the Rasa model
model:
	$(ECHO) "Training Rasa model..."
	$(call RASA_DOCKER_MODEL, train)

# Start Rasa Inspector with logging enabled
inspect:
	$(ECHO) "Starting Rasa Inspector with logging..."
	@$(MKDIR_LOG)
	$(call RASA_DOCKER, inspect --debug --log-file logs/logs.out)

# Start the Rasa server with logging enabled
run:
	$(ECHO) "Starting Rasa Server with logging..."
	@$(MKDIR_LOG)
	$(call RASA_DOCKER, run --debug --log-file logs/logs.out --enable-api --cors "*")

# Serve the chat widget and open it in the browser.
# Run this in a second terminal while `make run` is up (the widget talks to the
# Rasa server at http://localhost:5005). Press Ctrl+C to stop the widget server.
chat:
	$(ECHO) "Serving chat widget at http://localhost:$(CHAT_PORT) (Ctrl+C to stop)..."
	$(SERVE_WIDGET)

# Run end-to-end tests on the Rasa model
test:
	$(ECHO) "Testing Rasa model..."
	$(call RASA_DOCKER, test e2e tests/)
