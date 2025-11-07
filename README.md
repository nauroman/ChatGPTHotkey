# Text Improver Hotkey Script

A simple Python script that improves and corrects your text using OpenAI's GPT models with a single hotkey press.

## What It Does

Press your hotkey (default: `Ctrl+F13`) and the script will:
1. Select and copy all text in your active window
2. Send it to OpenAI's GPT model for improvement
3. Automatically paste the improved text back

Perfect for fixing grammar, improving clarity, and translating to polished American English.

---

## Quick Start

### 1. Get an OpenAI API Key

1. Go to [platform.openai.com](https://platform.openai.com/) and sign up/login
2. Click your profile → "View API Keys"
3. Click "Create New Secret Key" and copy it (starts with `sk-`)

### 2. Set Your API Key

**Windows:** Add it as an environment variable (recommended):
- Right-click Start → System → Advanced system settings → Environment Variables
- Click "New" under System variables
- Variable name: `OPENAI_API_KEY`
- Variable value: Your API key
- Click OK

**Verify:** Open Command Prompt and type `echo %OPENAI_API_KEY%`

### 3. Run the Script

**Easiest way:** Double-click `run_hotkey.bat` (installs dependencies automatically)

**Or run manually:**
```bash
python hotkey.py
```

The script will run in the background. Press `Ctrl+F13` to improve text in any application.

---

## Configuration

### Command Line Options

```bash
python hotkey.py --api_key YOUR_KEY --hotkey "<ctrl>+<f13>" --model gpt-4.1-nano --prompt "Your custom prompt"
```

- `--api_key`: Your OpenAI API key (optional if set in environment)
- `--hotkey`: Hotkey combination (default: `<ctrl>+<f13>`)
- `--model`: OpenAI model (default: `gpt-4.1-nano`)
- `--prompt`: Custom improvement instructions

### Edit Defaults in Code

Open `hotkey.py` in a text editor and find these lines:

```python
self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
self.model = model or "gpt-4.1-nano"
self.hotkey = hotkey or "<ctrl>+<f13>"
self.prompt = prompt or self.DEFAULT_PROMPT
```

Change the values after `or` to set new defaults.

### Hotkey Examples

- `<ctrl>+<f13>` (default)
- `<ctrl>+<shift>+h`
- `<alt>+<f2>`

Avoid common shortcuts like `Ctrl+C` to prevent conflicts.

---

## Model Selection

- **`gpt-4.1-nano` (default):** Fast, affordable, good for most tasks
- **`gpt-4o-mini`:** Better quality, slightly more expensive
- **`gpt-4o`:** Best quality for complex improvements

Check [OpenAI pricing](https://openai.com/pricing) for current rates.

---

## Auto-Start on Windows

### Method 1: Startup Folder (Simple)
1. Press `Win+R`, type `shell:startup`, press Enter
2. Drag `run_hotkey.bat` into the folder while holding Alt

### Method 2: Task Scheduler (Advanced)
1. Press `Win+R`, type `taskschd.msc`, press Enter
2. Click "Create Task"
3. Set trigger to "At log on"
4. Set action to run `run_hotkey.bat`

---

## Troubleshooting

**"API key not provided"**: Set the `OPENAI_API_KEY` environment variable or pass `--api_key`

**Hotkey doesn't work**: Try a different key combination, avoid conflicts with other programs

**"Another instance is already running"**: Only one instance can run at a time; close other instances

**Dependencies fail to install**: Manually install with:
```bash
pip install pyperclip pynput openai psutil
```

---

## Requirements

- Python 3.7+
- Windows OS (uses Windows keyboard API)
- OpenAI API key

Dependencies are auto-installed on first run.

---

## License

MIT License - See LICENSE file for details