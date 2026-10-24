@echo off
setlocal
cd /d "%~dp0"

REM Uses the existing OPENAI_API_KEY environment variable.
set "HOTKEY=<ctrl>+<f16>"
set "MODEL=gpt-6-luna"
set "REASONING_EFFORT=medium"

REM Fact-checking instructions and source validation live in factchecking.py.
python factchecking.py --hotkey "%HOTKEY%" --model "%MODEL%" --reasoning_effort "%REASONING_EFFORT%"
if errorlevel 1 pause
endlocal
