@echo off
setlocal
cd /d "%~dp0"
REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not available. No software was installed.
    pause
    exit /b 1
)

REM Set the OpenAI API key. If not provided, the environment variable OPENAI_API_KEY will be used.
set "API_KEY="

REM Set the hotkey to trigger the script. Default is ctrl+f13.
set "HOTKEY=<ctrl>+<f13>"
REM Edit in the original language with Ctrl+Shift+F13.
set "EDIT_HOTKEY=<ctrl>+<shift>+<f13>"

REM Set the OpenAI model to use. Default is gpt-5-nano.
set "MODEL=gpt-5-nano"

REM Leave prompts empty to use the built-in translation and editing instructions.
set "PROMPT="
set "EDIT_PROMPT="

REM Set the reasoning effort level. Options: minimal, low, medium, high. Leave empty for default (no reasoning parameter).
set "REASONING_EFFORT=minimal"

REM Keep an optional existing key out of the process command line.
if not "%API_KEY%"=="" set "OPENAI_API_KEY=%API_KEY%"

REM Run the hotkey.py script with the specified arguments.
python "%~dp0hotkey.py" --hotkey "%HOTKEY%" --edit_hotkey "%EDIT_HOTKEY%" --model "%MODEL%" --prompt "%PROMPT%" --edit_prompt "%EDIT_PROMPT%" --reasoning_effort "%REASONING_EFFORT%"

pause
