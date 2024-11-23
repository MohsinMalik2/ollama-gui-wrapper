# Ollama GUI Wrapper

This is a GUI-based application that allows users to interact with locally installed AI models via the `ollama` tool. It provides a clean interface for selecting a model, sending messages, and receiving responses.

## Features

- **Model Selection**: Automatically fetches and displays available models.
- **User-Friendly Interface**: Chat with models using a simple graphical interface.
- **Asynchronous Processing**: Ensures smooth user experience by avoiding that CLI confusing view.

## Requirements

- **Python**: Version 3.7 or later.
- **ollama**: Installed and configured on your system.
- **Python Libraries**: `tkinter`, `subprocess`, and `threading` (all are part of Python's standard library).
- **Icon File**: `chatbot.ico` in the project directory.

## Setup and Installation

1. **Clone or Download the Repository**:
   ```bash
   git clone https://github.com/MohsinMalik2/ollama-gui-wrapper.git
   cd ollama-gui-wrapper

2. **Add the Icon File**:
   Place your `chatbot.ico` file in the project directory. This icon will be used for the application window and executable.

3. **Install `ollama`**:
   Make sure `ollama` is installed on your system. Follow the official instructions to set it up:
   ```bash
   curl -sSf https://ollama.ai/install.sh | sh

4. **Verify Model Installation:**
    Use the following command to check the list of installed models:
    ```bash
    ollama list
    ```

    If no models are available, install one using:
    ```bash
    ollama install <model-name>
    ```

    Replace <model-name> with the desired model (e.g., llama3 or qwen-2.5-coder).

5. **Run the Application:**
    Launch the app by running:

    ```bash
    python app.py
    ```
    
    Interact:

    1. Select the model you want to use from the dropdown.
    2. Type your message in the input box and press Send.
    3. View the conversation in the chat display area.


    