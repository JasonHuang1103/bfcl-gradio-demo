---
title: BFCL Visualization Test
emoji: 🔥
colorFrom: pink
colorTo: yellow
sdk: gradio
sdk_version: 5.8.0
app_file: app.py
pinned: false
---

# Overview
This project implements a comparison tool for evaluating and visualizing responses from different LLMs. The system processes JSON results from model interactions and provides an interactive interface for analysis.

## Core Components
- app.py 
- const.py
- standardize.py
- state.py

---

### app.py
The main application module that creates the Gradio interface for model comparison visualization.

**Key Features:**
- Creates an interactive web interface using Gradio
- Provides model selection dropdowns for comparison
- Displays conversation turns side by side
- Enables navigation through conversation history
- Shows token counts and other metrics

**Main Components:**
[to be updated]

---

### const.py
Configuration and constant definitions for the project.

**Key Features:**
* Defines file paths and directory structures
* Lists available models for comparison
* Sets default model configurations
* Maintains model name mappings and constants

**Key Fields of Input Json Structure:**
* id: identifier for the conversation
* result: array of turns, each containing tool calls and response
* inference_log: (optional) logging information
* input_token_count: token counts for input
* output_token_count: token counts for output
* latency: (optional) response time measurements

---

### standardize.py
Handles data standardization and processing of model outputs.

**Key Features:**
* Reads and processes JSON Lines (JSONL) format result files
* Standardizes model responses for consistent comparison
* Handles optional fields in the data structure
* Provides error handling for missing or malformed data

**Main Functions:**
* get_result(): Reads and processes JSONL files into pandas DataFrames
* standardize_inference_response(): Normalizes response format with optional fields

---

### state.py
The state management module that handles the comparison logic between two models.

**Key Features:**
* Maintains the current state of comparison between two models
* Processes turn-by-turn and step-by-step responses
* Handles model response formatting and display
* Calculates and tracks progress through conversation turns

**Main Classes:**
* State: Manages the comparison state between two models
    * update_entry(): Updates the current entry being compared
    * get_step_response(): Processes individual response steps
    * format_step_response(): Standardizes response format for display



Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference


