# Text Improver ChatGPT Hotkey Script

A simple yet powerful Python script to automatically translate and/or improve your text using OpenAI's GPT models. Perfect for quickly fixing grammar, syntax, idioms, and polishing your writing into clear, polite, educated American English—all with a single hotkey press.

## Why Use This Script?
- **Instant Text Enhancement:** Translate and/or improve your writing in seconds with one keystroke.
- **Seamless Workflow:** Copies, enhances, and pastes text automatically—no manual steps needed.
- **Fully Customizable:** Adjust the hotkey, GPT model, and improvement prompt to suit your needs.

## How It Works
When you press the predefined hotkey (default: `Ctrl+F13`):
1. The script selects all text (`Ctrl+A`) and copies it (`Ctrl+C`).
2. It sends the text to OpenAI's GPT model for improvement.
3. The improved text is pasted back (`Ctrl+V`) into your document or editor automatically.

---

## Installation

### Download the ZIP file from GitHub and extract it manually
https://github.com/nauroman/ChatGPTHotkey/archive/refs/heads/master.zip

### Or Clone the Repository

1. **If you don’t have Git:**, download it from [git-scm.com](https://git-scm.com/downloads) and install it.
2. **Open Command Prompt:** Windows key + R, type `cmd`, press Enter.
3. **Clone the Repository:** Type the following and press Enter:
   ```bash
   git clone https://github.com/nauroman/ChatGPTHotkey.git
   cd ChatGPTHotkey
   ```
---

## Getting Started: How to Get an OpenAI API Key
You’ll need an OpenAI API key to use this script. Here’s how to get one:

1. **Sign Up:** Go to [platform.openai.com](https://platform.openai.com/) and create an account (or log in).
2. **Navigate to API Keys:** Once logged in, click your profile (top-right), then select "View API Keys."
3. **Create a Key:** Click "Create New Secret Key," give it a name (e.g., "ChatGPTHotkey"), and click "Create."
4. **Copy the Key:** A key starting with `sk-` will appear. Copy it immediately—it won’t show again! Save it somewhere safe (e.g., a text file).

---

## Adding Your OpenAI API Key to Windows Environment Variables
To avoid hardcoding your API key in the script (safer and cleaner), add it to Windows:

1. **Open System Settings:**
   - Right-click the Start button, select "System."
   - Scroll down and click "Advanced system settings."
   - Click the "Environment Variables" button.
2. **Add the Key:**
   - In the "System variables" section, click "New."
   - Variable name: `OPENAI_API_KEY`
   - Variable value: Paste your API key (e.g., `sk-xxxx`).
   - Click "OK" on all open windows to save.
3. **Verify:** Reopen Command Prompt and type `echo %OPENAI_API_KEY%`. If it shows your key, it’s set!

---
## Running the Script

### Option 1: With Batch File (Windows)

Double-click `run_hotkey.bat` or run it from Command Prompt.

*Note:* First time it might be slow as it installs python and dependencies.


### Option 2: Without Batch File

### Step 1: Install Python
1. **Download Python:** Go to [python.org](https://www.python.org/downloads/), download the latest version (3.7 or higher), and run the installer.
2. **Important:** During installation, check the box "Add Python to PATH" before clicking "Install Now."
3. **Verify Installation:** Open Command Prompt (Windows key + R, type `cmd`, press Enter) and type `python --version`. If it shows a version number, you're good!

### Step 2: Run script
1. Open Command Prompt.
2. Navigate to the script folder: `cd path\to\ChatGPTHotkey`.
3. Run for default settings:
   ```bash
   python hotkey.py
   ```
4. Or run with custom settings:
   ```bash
   python hotkey.py --api_key YOUR_API_KEY --hotkey "<ctrl>+<f13>" --model gpt-5-nano --prompt "Improve this text to sound clear, polite, and professional in American English. Translate into English if necessary. The GPT should not ask for clarification; it should simply provide the corrected text without any introductions or additions such as 'here is the improved version.' Text to correct:"
   ```
   *Note:* Skip `--api_key` if it’s in environment variables.

---
## Configuration Options

You can tweak the script in two ways: editing `hotkey.py` directly or using `run_hotkey.bat`. Below are detailed instructions for both.

### Option 1: Direct Configuration (`hotkey.py`)
Open `hotkey.py` in a text editor (e.g., Notepad) and adjust these settings in the `hotkey.py`:

```python
self.settings = {
    "api_key": "YOUR_OPENAI_API_KEY",  # Replace with your key or leave blank if using environment variables
    "model": "gpt-5-nano",           # See "Choosing a Model" below
    "hotkey": "<ctrl>+<f13>",         # See "Changing the Hotkey" below
    "prompt": "Improve this text to sound clear, polite, and professional in American English. Translate into English if necessary. The GPT should not ask for clarification; it should simply provide the corrected text without any introductions or additions such as 'here is the improved version.' Text to correct:"  # See "Customizing the Prompt" below
}
```

### Option 2: Using a Batch File (`run_hotkey.bat`)
Edit `run_hotkey.bat` with Notepad and set these variables:

```batch
set "API_KEY=YOUR_OPENAI_API_KEY"
set "HOTKEY=<ctrl>+<f13>"
set "MODEL=gpt-5-nano"
set "PROMPT=Improve this text to sound clear, polite, and professional in American English. Translate into English if necessary. The GPT should not ask for clarification; it should simply provide the corrected text without any introductions or additions such as 'here is the improved version.' Text to correct:"
```

---

## Changing the Hotkey
The default hotkey is `Ctrl+F13`, but you can change it to something more convenient.

### How to Change It:
- **In `hotkey.py`:** Edit the `"hotkey"` line (e.g., `"<ctrl>+<shift>+h"`).
- **In `run_hotkey.bat`:** Edit the `HOTKEY` variable (e.g., `set "HOTKEY=<alt>+<f2>"`).
- **Examples:**
  - `<ctrl>+<shift>+h`: Ctrl + Shift + H
  - `<alt>+<f2>`: Alt + F2
  - `<ctrl>+t`: Ctrl + T

*Tip:* Avoid common hotkeys like `Ctrl+C` or `Ctrl+V` to prevent conflicts with other programs.

---

## Choosing a Model
The script uses OpenAI’s GPT models. Here’s a breakdown to help you pick:

- **`gpt-5-nano` (Default):**
  - **Performance:** Fast and good for most tasks (grammar, clarity, tone).
  - **Pricing:** Cheaper (~$0.15 per 1M input tokens, $0.60 per 1M output tokens as of March 2025).
  - **Best For:** Everyday use, quick edits.
- **`gpt-5`:**
  - **Performance:** More powerful, better at complex tasks (e.g., creative rewriting).
  - **Pricing:** More expensive (~$5 per 1M input tokens, $15 per 1M output tokens).
  - **Best For:** High-quality, nuanced improvements.

*How to Change:* Update `"model"` in `hotkey.py` or `MODEL` in `run_hotkey.bat`. Check [OpenAI’s pricing page](https://openai.com/pricing) for the latest rates.

---

## Customizing the Prompt
The prompt tells the GPT model how to improve your text. The default is:
- `"The GPT's role is to correct texts to reflect educated polite American English, 
                        adjusting grammar, syntax, and idioms while preserving meaning. 
                        Translate into English if necessary. It should maintain clarity, accuracy, 
                        and a neutral tone, avoiding unnecessary changes or complex vocabulary. 
                        The GPT should not ask for clarification; it should simply provide the 
                        corrected text without any introductions or additions such as 
                        'here is the improved version.' Text to correct:"`

### How to Change It:
- **In `hotkey.py`:** Edit the `"prompt"` line.
- **Or in `run_hotkey.bat`:** Edit the `PROMPT` variable.

### Prompt Ideas for Different Tasks:
- **Casual Tone:** `"Rewrite this text to sound friendly and informal. The GPT should not ask for clarification; it should simply provide the 
                        corrected text without any introductions or additions such as 
                        'here is the improved version.' Text to correct:"`
- **Technical Clarity:** `"Make this text concise and clear for a technical audience. The GPT should not ask for clarification; it should simply provide the 
                        corrected text without any introductions or additions such as 
                        'here is the improved version.' Text to correct:"`
- **Creative Writing:** `"Enhance this text with vivid, imaginative language. The GPT should not ask for clarification; it should simply provide the 
                        corrected text without any introductions or additions such as 
                        'here is the improved version.' Text to correct:"`

*Tip:* Experiment with prompts to match your specific needs!

---

## Adding to Windows Startup (Autorun)
Make the script run automatically when Windows starts. Here are two easy methods:

### Method 1: Startup Folder
1. **Open Startup Folder:** Windows key + R, type `shell:startup`, press Enter.
2. **Create Shortcut:** Drag `run_hotkey.bat` into the folder while holding Alt to create a shortcut.
3. **Test:** Restart your PC—it should start automatically.

### Method 2: Task Scheduler
1. **Open Task Scheduler:** Windows key + R, type `taskschd.msc`, press Enter.
2. **Create Task:**
   - Click "Create Task" (right panel).
   - Name it (e.g., "ChatGPTHotkey").
   - Check "Run with highest privileges."
3. **Trigger:**
   - Tab "Triggers," click "New."
   - Select "At log on," click "OK."
4. **Action:**
   - Tab "Actions," click "New."
   - Action: "Start a program."
   - Program/script: `C:\path\to\run_hotkey.bat` (adjust the path).
   - Click "OK."
5. Save: Click "OK," enter your password if prompted.

---

## Example Use Case
You’ve drafted a rough email:
- *Original:* "Hey, can u fix this quick? Thx."
- Press your hotkey (e.g., `Ctrl+F13`).
- *Improved:* "Hello, could you please address this at your earliest convenience? Thank you!"

---

## Troubleshooting
- **API Key Errors:** Double-check your key in `hotkey.py`, `run_hotkey.bat`, or environment variables.
- **Hotkey Not Working:** Ensure it’s not conflicting with another program; try a different combo.
- **Dependencies Fail:** Install manually:
  ```bash
  pip install pyautogui pyperclip pynput openai
  ```

---

## License
Distributed under the MIT License. See `LICENSE` for more details.

---

This version is now much more detailed and beginner-friendly, covering every step with clarity and actionable guidance. Let me know if you’d like further tweaks!