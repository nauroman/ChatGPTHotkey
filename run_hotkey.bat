@echo off
REM Set the OpenAI API key. If not provided, the environment variable OPENAI_API_KEY will be used.
set "API_KEY="

REM Set the hotkey to trigger the script. Default is ctrl+f13.
set "HOTKEY=<ctrl>+<f13>"

REM Set the OpenAI model to use. Default is gpt-4o-mini.
set "MODEL=gpt-4o-mini"

REM Set the prompt for the OpenAI model. Default prompt is provided.
set "PROMPT=The GPT's role is to correct texts to reflect educated polite American English, adjusting grammar, syntax, and idioms while preserving meaning. Translate into English if necessary. It should maintain clarity, accuracy, and a neutral tone, avoiding unnecessary changes or complex vocabulary. The GPT should not ask for clarification; it should simply provide the corrected text without any introductions or additions such as 'here is the improved version.' Text to correct:"

REM Initialize the arguments string
set "ARGS="

if not "%API_KEY%"=="" set "ARGS=%ARGS% --api_key %API_KEY%"
if not "%HOTKEY%"=="" set "ARGS=%ARGS% --hotkey "%HOTKEY%""
if not "%MODEL%"=="" set "ARGS=%ARGS% --model %MODEL%"
if not "%PROMPT%"=="" set "ARGS=%ARGS% --prompt "%PROMPT%""

REM Run the hotkey.py script with the specified arguments.
python hotkey.py %ARGS%

pause