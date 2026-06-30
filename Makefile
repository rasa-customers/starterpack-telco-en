# Your Rasa version
RASA_VERSION := 3.16.10

# Port used by `make chat` to serve the chat widget
CHAT_PORT := 8000

# Default e2e test path. Override to run a subset, e.g.
#   make test TEST_PATH="tests/e2e_test_cases/billing_test_cases.yml"
TEST_PATH ?= tests/

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
HELP_inspect := Launch Inspector + Rasa + actions and open it in the browser
HELP_run     := Start the Rasa server only (API enabled, no UI)
HELP_chat    := Launch chat widget + Rasa + actions and open it in the browser
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
  # `make chat` pre-launch: serve the widget, then open it after a short delay.
  CHAT_PRELAUNCH = Start-Process python -ArgumentList '-m','http.server','$(CHAT_PORT)','--directory','chatwidget' -WindowStyle Hidden; Start-Job { Start-Sleep 10; Start-Process 'http://localhost:$(CHAT_PORT)' } | Out-Null;
  # `make inspect` pre-launch: open the Inspector after a short delay.
  INSPECT_PRELAUNCH = Start-Job { Start-Sleep 10; Start-Process 'http://localhost:5005/webhooks/socketio/inspect.html' } | Out-Null;
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
  # `make chat` pre-launch: serve the widget in the background, open it once the
  # Rasa server answers on :5005 (so the greeting fires), and stop the widget
  # server on exit. Ends with `&` so the docker run that follows is foreground.
  CHAT_PRELAUNCH = python3 -m http.server $(CHAT_PORT) --directory chatwidget >logs/widget.log 2>&1 & WIDGET_PID=$$!; trap 'kill $$WIDGET_PID 2>/dev/null' EXIT INT TERM; ( for _ in $$(seq 1 90); do curl -sf -o /dev/null http://localhost:5005/ && break; sleep 1; done; $(OPEN_URL) "http://localhost:$(CHAT_PORT)" ) &
  # `make inspect` pre-launch: open the Inspector once Rasa answers on :5005.
  INSPECT_PRELAUNCH = ( for _ in $$(seq 1 90); do curl -sf -o /dev/null http://localhost:5005/ && break; sleep 1; done; $(OPEN_URL) "http://localhost:5005/webhooks/socketio/inspect.html" ) &
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

# Start the Rasa Inspector (Rasa server + in-process actions) and open it.
inspect:
	$(ECHO) "Starting Rasa Inspector (Rasa + in-process actions). Ctrl+C to stop..."
	@$(MKDIR_LOG)
	@$(INSPECT_PRELAUNCH) $(call RASA_DOCKER, inspect --debug --log-file logs/logs.out)

# Start the Rasa server with logging enabled
run:
	$(ECHO) "Starting Rasa Server with logging..."
	@$(MKDIR_LOG)
	$(call RASA_DOCKER, run --debug --log-file logs/logs.out --enable-api --cors "*")

# Start everything for the demo in one command: the Rasa server (with in-process
# actions) plus the chat widget, then open the widget once Rasa is ready.
# Ctrl+C stops both.
chat:
	$(ECHO) "Starting chat widget + Rasa (with in-process actions). Ctrl+C to stop..."
	@$(MKDIR_LOG)
	@$(CHAT_PRELAUNCH) $(call RASA_DOCKER, run --debug --log-file logs/logs.out --enable-api --cors "*")

# Run end-to-end tests on the Rasa model (override TEST_PATH to run a subset)
test:
	$(ECHO) "Testing Rasa model..."
	$(call RASA_DOCKER, test e2e $(TEST_PATH))
