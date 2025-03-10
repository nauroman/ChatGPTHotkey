# Text Improver Hotkey Script

A simple yet powerful Python script to automatically improve your selected text using OpenAI's GPT models. Ideal for quickly correcting grammar, syntax, idioms, and enhancing the clarity of your texts with educated, polite American English.

## Why Use This Script?
- **Quick Text Improvement:** Instantly enhance your writing with a single hotkey.
- **Efficient Workflow:** Automatically copies, improves, and pastes your text without manual intervention.
- **Highly Customizable:** Easily configure your preferred hotkey, GPT model, and custom prompts.

## How It Works
Upon pressing a predefined hotkey (Ctrl+F13 by default):
1. The script selects all text (`Ctrl+A`) and copies it (`Ctrl+C`).
2. It sends the copied text to OpenAI's GPT model for improvement.
3. The improved text is automatically pasted back (`Ctrl+V`) into your document or editor.

---

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/text-improver.git
cd text-improver
```

### Step 2: Install Dependencies
Ensure you have Python installed (3.7+). Then, run:
```bash
pip install -r requirements.txt
```

**Note:** If dependencies are missing, the script attempts to install them automatically upon the first run.

---

## Configuration

You can configure the script directly in the Python file (`hotkey.py`) or by using a batch file (`run_hotkey.bat`).

### Direct Configuration (`hotkey.py`)

Adjust settings in the `TextImprover` class:

```python
self.settings = {
    "api_key": "YOUR_OPENAI_API_KEY",  # Set your API key here or via the OPENAI_API_KEY environment variable
    "model": "gpt-4o-mini",           # Choose your preferred GPT model
    "hotkey": "<ctrl>+<f13>",          # Set your desired hotkey
    "prompt": "Your custom prompt here..."  # Customize the prompt to your needs
}
```

### Using a Batch File (`run_hotkey.bat`)

Edit the following variables in `run_hotkey.bat`:

```batch
set "API_KEY=YOUR_OPENAI_API_KEY"
set "HOTKEY=<ctrl>+<f13>"
set "MODEL=gpt-4o-mini"
set "PROMPT=Your custom prompt here..."
```

---

## Running the Script

### Without Batch File (Directly)
Run the script directly from your terminal or command prompt:
```bash
python hotkey.py --api_key YOUR_API_KEY --hotkey "<ctrl>+<f13>" --model gpt-4o-mini
```

You can omit arguments if you've set them directly in the Python script or environment variables.

### With Batch File (Recommended for Windows Users)

Double-click the `run_hotkey.bat` file or run it from a command prompt:
```batch
run_hotkey.bat
```

---

## Customizing the Hotkey

The default hotkey is set to `<ctrl>+<f13>`. Change it easily by editing the `HOTKEY` setting in either the Python or batch file. Examples:
- `<ctrl>+<shift>+h`
- `<alt>+<f2>`

---

## Example Use Case
Imagine you've quickly drafted an important email or document but want to ensure it reads professionally. Simply:

1. Select the text you wrote (or let the script select all automatically).
2. Press your predefined hotkey.
3. Enjoy the instantly improved text, pasted back automatically.

---

## Troubleshooting

- **API Key Errors:** Ensure your API key is correctly set.
- **Dependency Issues:** Manually install any missing dependencies using:
  ```bash
  pip install pyautogui pyperclip pynput openai
  ```

---

## License

Distributed under the MIT License. See `LICENSE` for more details.

