@echo off
REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Installing Python...
    REM Download Python installer
    curl -o python-installer.exe https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe
    REM Install Python silently
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    REM Clean up installer
    del python-installer.exe
)

REM Set the OpenAI API key. If not provided, the environment variable OPENAI_API_KEY will be used.
set "API_KEY="

REM Set the hotkey to trigger the script. Default is ctrl+shift+f13.
set "HOTKEY=<ctrl>+<f16>"

REM Set the OpenAI model to use. Default is a GPT-5 thinking-capable model.
set "MODEL=gpt-5.2"

REM Set the prompt for the OpenAI model to perform fact-checking.
set "PROMPT=You are a rigorous fact-checking assistant. Start with a very brief overall conclusion: true or false. Then provide detailed explanations for each point. Use only reliable, well-established sources (prefer official or primary sources). For every verifiable claim, state whether it is accurate, partially accurate, or inaccurate, cite the supporting source URLs, and briefly explain why. If a claim cannot be confirmed with trusted sources, state that it cannot be verified and warn the reader not to rely on it. Keep the entire response concise and to the point. Respond in the same language as the input text. Provide plain text output with clear sentences and include URLs inline. Text to fact-check:"

REM Set the reasoning effort level. Options: minimal, low, medium, high. Leave empty for default (no reasoning parameter).
set "REASONING_EFFORT=medium"

REM Initialize the arguments string
set "ARGS="

if not "%API_KEY%"=="" set ARGS=%ARGS% --api_key %API_KEY%
if not "%HOTKEY%"=="" set ARGS=%ARGS% --hotkey "%HOTKEY%"
if not "%MODEL%"=="" set ARGS=%ARGS% --model %MODEL%
if not "%PROMPT%"=="" set ARGS=%ARGS% --prompt "%PROMPT%"
if not "%REASONING_EFFORT%"=="" set ARGS=%ARGS% --reasoning_effort %REASONING_EFFORT%

REM Run the hotkey.py script with the specified arguments.
python hotkey.py %ARGS%

pause
