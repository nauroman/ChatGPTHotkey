# ChatGPTHotkey

**Turn a rough draft into clearer writing without moving it into a chat window.**

ChatGPTHotkey brings English translation and original-language editing to compatible Windows text fields. Stay in your editor, press a shortcut, and replace the draft with the result. Use it when you have something to say and want help saying it well.

**[Download the source ZIP](https://github.com/nauroman/ChatGPTHotkey/archive/refs/heads/master.zip)** · [Quick start](#quick-start-windows) · [Browse the code](https://github.com/nauroman/ChatGPTHotkey)

This is a Python source project, not a packaged installer. It uses the OpenAI API, with separate API billing; a ChatGPT subscription does not cover these requests.

## Two writing modes

| Shortcut | Result |
| --- | --- |
| **Ctrl+F13** | Translate into natural, polished American English. If the input is already English, correct and refine it. |
| **Ctrl+Shift+F13** | Edit in the original language: correct errors and improve clarity, vocabulary, expression and sentence flow. Russian stays Russian; English stays English. |

The goal is writing that sounds thoughtful, articulate and natural, without unnecessary formality or inflated wording. Both prompts ask the model to preserve your meaning, facts, tone and formatting, and not invent details or commitments. The result is ready-to-use text, without a preamble.

### What that looks like

These are short excerpts from manual checks in a disposable text field, not guarantees of identical output on every request.

| Mode | Before | After |
| --- | --- | --- |
| English translation | Я не обещал закончить работу к пятнице. | I did not promise to finish the work by Friday. |
| Russian editing | мне кажеться, идея хорошая но детали надо абсудить заранее. | Мне кажется, идея хорошая, но детали нужно обсудить заранее. |
| English editing | we has two ideas and i think they is worth discussing. | We have two ideas, and I think they are worth discussing. |

**Start with a disposable field.** The shortcut captures everything selected by Ctrl+A in that field or editor, sends it to OpenAI, and replaces it with plain text. It does not process only a passage you previously highlighted.

## Quick start: Windows

1. **Get the source.** [Download the ZIP](https://github.com/nauroman/ChatGPTHotkey/archive/refs/heads/master.zip) and extract it. If you prefer Git, use `git clone https://github.com/nauroman/ChatGPTHotkey.git`.
2. **Prepare Python and API access.** Install [Python for Windows](https://www.python.org/downloads/windows/) with `python` on `PATH`. For a fresh setup, use Python 3.10+ to meet the current SDK requirements. Privately set `OPENAI_API_KEY` in your Windows user environment variables. [API setup details](#configure-api-access) are below.
3. **Open a new Command Prompt in the extracted project folder** so it inherits the key, then run:

```bat
python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt
run_hotkey.bat
```

Leave that console running. Put a harmless sentence in a compatible text field, focus it, and try Ctrl+F13 or Ctrl+Shift+F13. No API key needs to be written into the repository.

If your keyboard has no F13, use the [custom-shortcut example](#configuration). For later sessions, reactivate the environment and start the launcher again:

```bat
call .venv\Scripts\activate.bat
run_hotkey.bat
```

## How the shortcuts work

The shortcuts are mutually exclusive. Processing starts when **F13 is released**; release the modifiers promptly too. Holding Shift selects editing rather than also triggering translation. Repeated presses during a request are ignored, and both modes share one processing lock.

The current default model is **`gpt-5-nano`**, with **`minimal`** reasoning effort. Both modes use the same model.

1. Focus the editable field you want to process.
2. Press and release the shortcut.
3. The script sends **Ctrl+A, then Ctrl+C** to capture all text in that field or editor.
4. It sends the captured text to the OpenAI API.
5. On a successful, non-empty, complete response, it sends **Ctrl+V** to replace the selection.

In a document editor, Ctrl+A may select the whole document.

Compatibility depends on the application's handling of these keyboard and clipboard shortcuts; custom editors may behave differently. Replacement is plain text, so rich formatting is not guaranteed. Keep the field and its contents unchanged while waiting. The script cancels insertion if the foreground window changes, but it does not track every focus change or edit within the same window.

## Requirements

- **Windows**: the script uses the Win32 keyboard API through `ctypes`.
- **Python and pip**, with `python` available on `PATH`. For a fresh installation, use **Python 3.10+**, as required by the [current OpenAI Python SDK](https://github.com/openai/openai-python#requirements). The repository itself does not pin a Python version or dependency versions; support also depends on the packages you install.
- An OpenAI API key with access to the configured model, network connectivity and available API quota.
- Git if you use the clone command below; downloading the repository as a ZIP is also possible.

The main script imports `pyperclip` for text clipboard access, `pynput` for hotkeys, and `openai` for API requests. Fact Checker also imports `httpx` for direct Responses API requests. [requirements.txt](requirements.txt) also lists `pyautogui` and `psutil`; these two packages are not currently imported by `hotkey.py`.

API use is billed separately from a ChatGPT subscription. See [OpenAI's billing explanation](https://help.openai.com/en/articles/9039756-managing-billing-for-chatgpt-and-the-api-platform) and [current API pricing](https://developers.openai.com/api/docs/pricing).

`run_hotkey.bat` checks for Python and exits with a message if it is unavailable; it does not install Python. `hotkey.py` still tries to install missing `pyperclip`, `pynput` or `openai` packages automatically with pip. Installing the requirements explicitly first avoids that bootstrap step.

## Configure API access

Use the **`OPENAI_API_KEY` environment variable**:

1. Open the Windows environment-variable settings for your user account.
2. Add `OPENAI_API_KEY` and enter your API key privately as its value.
3. Open a new Command Prompt so it inherits the variable, return to the project folder, and reactivate `.venv`.

Check only whether the variable is present, without displaying its value:

```bat
python -c "import os; print('Configured' if os.environ.get('OPENAI_API_KEY') else 'Missing')"
```

Manage API keys in your [OpenAI API account](https://platform.openai.com/api-keys). Do not put keys in Git, screenshots or issue reports. The script does **not** load `.env` files automatically.

The CLI also accepts `--api_key`, and the batch launcher has a legacy `API_KEY` setting. Prefer the environment variable: command-line keys may be visible in process arguments, and a key saved in the tracked batch file could be committed accidentally. Leave the launcher's `API_KEY` empty when using `OPENAI_API_KEY`.

## Start, stop and restart

From the project folder in the activated Command Prompt:

```bat
run_hotkey.bat
```

Or use the Python defaults directly:

```bat
python hotkey.py
```

Both provide the two default writing shortcuts. Leave the process running while you use them. Start only one writing instance: the processing lock belongs to each process and does not prevent duplicate copies of the program.

Press **Ctrl+C in that process's console**, or close that console, to stop its hotkey listener. The batch launcher may wait at its final `pause` after Python exits. Restart the process after changing configuration or code; there is no automatic reload.

The batch launcher uses whichever `python` is on `PATH`; it does not activate `.venv` itself. For the virtual-environment installation above, launch it from the activated terminal. A double-click or desktop shortcut may use a different Python environment. Any `.lnk` files in the repository are machine-specific; create your own shortcut for your installation rather than relying on their stored targets.

## Configuration

Edit these settings in [run_hotkey.bat](run_hotkey.bat), then restart:

| Setting | Default | Purpose |
| --- | --- | --- |
| `HOTKEY` | `<ctrl>+<f13>` | Primary English translation/correction shortcut. |
| `EDIT_HOTKEY` | `<ctrl>+<shift>+<f13>` | Original-language editing shortcut. |
| `MODEL` | `gpt-5-nano` | OpenAI model used by both modes. |
| `REASONING_EFFORT` | `minimal` | Reasoning effort for the selected model. |
| `PROMPT` | Empty | Use the built-in translation prompt; a non-empty value overrides it. |
| `EDIT_PROMPT` | Empty | Use the built-in editing prompt; a non-empty value overrides it. |

The corresponding CLI options are `--hotkey`, `--edit_hotkey`, `--model`, `--reasoning_effort`, `--prompt` and `--edit_prompt`. View the parser's help with:

```bat
python hotkey.py --help
```

For a keyboard without F13, configure two distinct shortcuts. For example:

```bat
python hotkey.py --hotkey "<ctrl>+<alt>+<f11>" --edit_hotkey "<ctrl>+<alt>+<f12>" --model gpt-5-nano --reasoning_effort minimal
```

Each shortcut needs exactly one non-modifier key. Extra modifiers do not match. When setting a custom primary shortcut through the CLI, also supply `--edit_hotkey` if you want both modes: the editing shortcut is added automatically only when the primary shortcut is the default `<ctrl>+<f13>`.

For `gpt-5-nano`, an omitted or empty reasoning-effort value falls back to `minimal`. Other models receive reasoning effort only when it is supplied. Accepted effort values depend on the model; changing a model or effort setting requires compatible API access. The code uses Responses when the installed SDK provides it and an effort is set, otherwise Chat Completions with the legacy-SDK fallback.

## Errors and diagnostics

Diagnostics go to the console and **`hotkey.log` beside `hotkey.py`**. The log rotates at 256 KiB with one backup. It records modes, model names, error categories and HTTP status, rather than source text or raw exception messages.

| Symptom | What to check |
| --- | --- |
| Missing API key at startup | Set `OPENAI_API_KEY`, then restart from a terminal that inherited it. |
| Authentication failure / HTTP 401 | Check that the existing credential is valid and available to this process. |
| Unavailable model / HTTP 404 | Check `MODEL` and account access to that model. |
| Exhausted API quota | Review API billing and usage limits; this is different from a temporary rate limit. |
| Rate limit | Wait before trying again. |
| Connection failure or timeout | Check connectivity. API requests use a 30-second SDK timeout with automatic SDK retries disabled. |
| Empty, refused or incomplete response | The result is rejected; retry if appropriate. |
| No text captured | Confirm focus is in a compatible editable field and Ctrl+A / Ctrl+C work there. |
| Active window changed | Insertion is cancelled; retry in the intended field. |
| Processing already in progress | Wait for the current request; repeated triggers are ignored. |

Request failures show a safe error message and do not intentionally replace the original text. If no text can be copied, the script returns without replacement. Diagnostics do not guarantee compatibility with every application, and ordinary model mistakes in meaning or style still need human review.

## Privacy and clipboard behavior

All captured text is sent to the OpenAI API; processing is not offline. Only invoke the shortcut on text you intend to send. Task instructions and source data are separated, and the prompts ask the model to transform embedded commands or questions as text rather than obey or answer them.

Clipboard handling is text-only: the script saves and restores clipboard **text**, not a full snapshot of images, rich text or other formats. Avoid changing the clipboard during a request. Do not include keys, private clipboard contents or sensitive source text when sharing diagnostics.

## Tests

With dependencies installed, run from the project folder on Windows:

```bat
python -m unittest discover -s tests -v
```

The [writing-mode tests](tests/test_hotkey.py) cover exact shortcut selection, press/release order, autorepeat, Unicode input, shared processing exclusion, prompt/source separation, errors, incomplete results, clipboard-text restoration and active-window cancellation. They use mocked API and desktop operations, do not require an API key, and do not make live API requests or append to the runtime log. Native application compatibility and translation quality need separate manual checks in a disposable field. The [Fact Checker tests](tests/test_factchecking.py) also cover source provenance, factual versus subjective verdicts, incomplete reports and failures without automatic retries.

## Additional launchers

### Fact Checker: Ctrl+F14

[run_factchecking.bat](run_factchecking.bat) starts a separate fact checker through [factchecking.py](factchecking.py), using **`gpt-6-luna` with `medium` reasoning and live web search**. Run it with the same prepared Python environment, then focus a disposable text field and press **Ctrl+F14**. As with the writing modes, it captures everything selected by Ctrl+A in that field and replaces it with the completed report.

The report distinguishes facts, opinions, predictions and uncertainty. Sourced factual verdicts require URLs returned by the current search response. This verifies URL provenance, not the truth of every interpretation; review important conclusions yourself. API failures, incomplete reports and unsupported evidence are rejected without replacing the original text.

**Web search is billed separately from model tokens.** A lower model token price does not guarantee a lower total cost than a mode without search. Latency varies with the passage, evidence and network; there is no universal speed guarantee. See [current API pricing](https://developers.openai.com/api/docs/pricing) and [Fact Checker settings and limits](FACTCHECKING.md).

The launcher uses the existing `OPENAI_API_KEY` and works from its own folder. The two writing modes keep their existing model and shortcuts.

[run_hotkey_poem.bat](run_hotkey_poem.bat) is a separate poem-writing configuration. It reuses **Ctrl+F13**, so it conflicts with the default writing instance. The poem launcher retains its legacy bootstrap behavior.
