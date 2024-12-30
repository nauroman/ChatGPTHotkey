# Text Improvement Hotkey Script

This project provides a script that uses OpenAI's API to improve text by correcting grammar, syntax, and idioms while preserving the original meaning. The script can be triggered using a hotkey.

## Requirements

- Python
- pip

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

1. Set your OpenAI API key in the `run_hotkey.bat` file or as an environment variable `OPENAI_API_KEY`.

2. Optionally, you can configure the hotkey, model, and prompt in the `run_hotkey.bat` file.

## Usage

1. Run the `run_hotkey.bat` file to start the script:
    ```sh
    run_hotkey.bat
    ```

2. The script will run in the background. Press the configured hotkey (default is `ctrl+f11`) to improve the text.

## Files

- `hotkey.py`: The main script that handles the hotkey and text improvement.
- `requirements.txt`: Lists the required Python packages.
- `.gitignore`: Specifies files and directories to be ignored by git.
- `run_hotkey.bat`: Batch file to set up and run the script.
- `settings.txt`: Optional file to load settings from.

## License

This project is licensed under the MIT License.