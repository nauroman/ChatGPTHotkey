# Text Improver & Fact Checker Hotkey Script

A versatile Python script that improves and corrects your text using OpenAI's GPT models with a single hotkey press. Now supports fact-checking with GPT-5 reasoning models.

## What It Does

Press your hotkey and the script will:
1. Select and copy all text in your active window
2. Send it to OpenAI's GPT model for processing
3. Automatically paste the result back

**Two modes available:**
- **Text Improvement** (default): Fix grammar, improve clarity, translate to polished American English
- **Fact Checking**: Verify claims with reliable sources, cite URLs, and provide accuracy assessments

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

**Text Improvement Mode (default):**
- Double-click `run_hotkey.bat` (installs dependencies automatically)
- Press `Ctrl+F13` to improve text in any application

**Fact Checking Mode:**
- Double-click `run_factchecking.bat`
- Press `Ctrl+F16` to fact-check text in any application

**Or run manually:**
```bash
python hotkey.py
```

The script will run in the background.

---

## Configuration

### Command Line Options

```bash
python hotkey.py --api_key YOUR_KEY --hotkey "<ctrl>+<f13>" --model gpt-4.1-nano --prompt "Your custom prompt" --reasoning_effort medium
```

- `--api_key`: Your OpenAI API key (optional if set in environment)
- `--hotkey`: Hotkey combination (default: `<ctrl>+<f13>`)
- `--model`: OpenAI model (default: `gpt-4.1-nano`)
- `--prompt`: Custom improvement instructions
- `--reasoning_effort`: Reasoning level (`low`, `medium`, `high`) - enables GPT reasoning models for complex tasks

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

- **`gpt-4.1-nano` (default):** Fast, affordable, good for most text improvement tasks
- **`gpt-4o-mini`:** Better quality, slightly more expensive
- **`gpt-4o`:** High quality for complex improvements
- **`gpt-5`:** Advanced reasoning capabilities for fact-checking and complex analysis

Check [OpenAI pricing](https://openai.com/pricing) for current rates.

## Fact Checking Mode

The fact checking mode uses GPT-5 reasoning models to verify claims in your text:

**Features:**
- Verifies each claim using reliable, well-established sources
- Cites source URLs for transparency
- States accuracy level: accurate, partially accurate, or inaccurate
- Warns when claims cannot be verified
- Responds in the same language as input

**How to use:**
1. Run `run_factchecking.bat`
2. Select text containing claims you want to verify
3. Press `Ctrl+F16` (default hotkey)
4. The text will be replaced with a fact-checked version including sources

**Customize fact checking:**
Edit `run_factchecking.bat` to change:
- `HOTKEY`: Change the hotkey (default: `<ctrl>+<f16>`)
- `MODEL`: Change the model (default: `gpt-5`)
- `REASONING_EFFORT`: Adjust reasoning depth (`low`, `medium`, `high`)
- `PROMPT`: Modify fact-checking instructions

---

## Auto-Start on Windows

### Method 1: Startup Folder (Simple)
1. Press `Win+R`, type `shell:startup`, press Enter
2. Create shortcuts for the modes you want:
   - Drag `run_hotkey.bat` (text improvement) while holding Alt
   - Drag `run_factchecking.bat` (fact checking) while holding Alt

### Method 2: Task Scheduler (Advanced)
1. Press `Win+R`, type `taskschd.msc`, press Enter
2. Click "Create Task"
3. Set trigger to "At log on"
4. Set action to run your preferred `.bat` file

---

## Troubleshooting

**"API key not provided"**: Set the `OPENAI_API_KEY` environment variable or pass `--api_key`

**Hotkey doesn't work**: Try a different key combination, avoid conflicts with other programs

**Running both modes simultaneously**: You can run both `run_hotkey.bat` and `run_factchecking.bat` at the same time with different hotkeys

**Dependencies fail to install**: Manually install with:
```bash
pip install pyperclip pynput openai
```

**Fact checking gives errors**: Ensure you have access to GPT-5 models in your OpenAI account

---

## Requirements

- Python 3.7+
- Windows OS (uses Windows keyboard API)
- OpenAI API key

Dependencies are auto-installed on first run.

---

## License

MIT License - See LICENSE file for details