# -------------------------------------------------------------
# Makefile for interactive Plotly dashboard (cross-platform)
# -------------------------------------------------------------

# Configuration
VENV := .venv
PYTHON := python3
SRC_DIR := src
DATA_DIR := data

# OS detection (Windows vs Unix)
ifeq ($(OS),Windows_NT)
	ACTIVATE := $(VENV)/Scripts/activate
	PY := $(VENV)/Scripts/python
	JUP := $(VENV)/Scripts/jupyter
else
	ACTIVATE := $(VENV)/bin/activate
	PY := $(VENV)/bin/python
	JUP := $(VENV)/bin/jupyter
endif

# -------------------------------------------------------------
# Default target
# -------------------------------------------------------------
all: setup

# -------------------------------------------------------------
# Setup: create virtual environment and install dependencies
# -------------------------------------------------------------
setup:
	@echo "🛠️  Setting up Python virtual environment..."
	$(PYTHON) -m venv $(VENV)
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -r requirements.txt
	@echo "✅ Setup complete. Activate manually with:"
	@echo "   source $(ACTIVATE)"

# -------------------------------------------------------------
# Enable Jupyter widgets (for Plotly + ipywidgets)
# -------------------------------------------------------------
enable-widgets:
	@echo "🔧 Enabling Jupyter widgets..."
ifeq ($(OS),Windows_NT)
	$(PY) -m jupyter nbextension enable --py widgetsnbextension --sys-prefix || exit 0
else
	$(PY) -m jupyter nbextension enable --py widgetsnbextension --sys-prefix || true
endif
	@echo "✅ Widgets enabled."

# -------------------------------------------------------------
# Run Jupyter Notebook
# -------------------------------------------------------------
notebook:
	@echo "🚀 Launching Jupyter Notebook..."
	$(JUP) notebook

# -------------------------------------------------------------
# Run interactive plot script directly
# -------------------------------------------------------------
run:
	@echo "📊 Running interactive_plot.py..."
	$(PY) $(SRC_DIR)/interactive_plot.py

# -------------------------------------------------------------
# One-step dashboard launcher
# -------------------------------------------------------------
run-dashboard:
	@echo "🚀 Launching Jupyter Notebook with dashboard ready..."
	$(JUP) notebook $(SRC_DIR)/interactive_plot.py

# -------------------------------------------------------------
# Clean up environment
# -------------------------------------------------------------
clean:
	@echo "🧹 Cleaning up..."
	rm -rf $(VENV) __pycache__ */__pycache__ .ipynb_checkpoints
	@echo "✅ Cleaned virtual environment and caches."
