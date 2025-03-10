import sys
import subprocess
import os
import time
import psutil
import pyautogui
from pynput.keyboard import GlobalHotKeys, Key, Controller as KeyboardController
import pyperclip
from openai import OpenAI

# Auto-install required packages
required_packages = ['psutil', 'pynput', 'pyperclip', 'openai', 'pyautogui']
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# Configuration and client setup
settings = {
    "api_key": os.environ.get("OPENAI_API_KEY"),
    "model": "gpt-4o-mini",
    "hotkey": "ctrl+f13",
    "prompt": "The GPT's role is to correct texts to reflect educated polite American English, adjusting grammar, syntax, and idioms while preserving meaning. Translate into English if necessary. It should maintain clarity, accuracy, and a neutral tone, avoiding unnecessary changes or complex vocabulary. The GPT should not ask for clarification; it should simply provide the updated text without any introductions or additions such as 'here is the improved version.' Text to correct :"
}

if not settings["api_key"]:
    print("Error: OPENAI_API_KEY environment variable is not set.")
    sys.exit(1)

client = OpenAI()
keyboard = KeyboardController()
listener = None


def improve_text(text: str) -> str:
    prompt = f"{settings['prompt'].strip()}\n\n{text}"

    try:
        completion = client.chat.completions.create(
            model=settings["model"],
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return text


def on_activate():
    global listener
    if listener:
        listener.stop()

    print("on_activate")
  #  pyperclip.copy('')
   # pyautogui.sleep(0.2)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.sleep(0.2)  # small delay to ensure clipboard updates
    pyautogui.hotkey("ctrl", "c")
    pyautogui.sleep(0.2)  # small delay to ensure clipboard updates
    text = pyperclip.paste()
    if not text:
        start_listener()
        return  # No text found in clipboard

    improved = improve_text(text)

    pyperclip.copy(improved)
    pyautogui.hotkey("ctrl", "v")
    # time.sleep(0.2)
    # pyperclip.copy('')
    # time.sleep(0.2)

  #  start_listener()


    # try:
    #     # Clear clipboard before operations
    #     pyperclip.copy('')
    #     time.sleep(0.2)
    #
    #     # Select all and copy
    #     with keyboard.pressed(Key.ctrl):
    #         keyboard.press('a')
    #         keyboard.release('a')
    #     time.sleep(0.2)
    #
    #     with keyboard.pressed(Key.ctrl):
    #         keyboard.press('c')
    #         keyboard.release('c')
    #     time.sleep(0.2)
    #
    #     original_text = pyperclip.paste()
    #     improved_text = improve_text(original_text)
    #
    #     # Copy improved text and paste
    #     pyperclip.copy(improved_text)
    #     time.sleep(0.2)
    #
    #     with keyboard.pressed(Key.ctrl):
    #         keyboard.press('v')
    #         keyboard.release('v')
    #     time.sleep(0.2)
    #
    #     # Clear clipboard after operations
    #     pyperclip.copy('')
    #
    # except Exception as e:
    #     print(f"Processing Error: {e}")
    # finally:
    #     start_listener()


def start_listener():
    global listener
    hotkey = '+'.join(f'<{part}>' for part in settings["hotkey"].split('+'))
    listener = GlobalHotKeys({hotkey: on_activate})
    listener.start()


# Add this function before the main code
def kill_other_instances():
    current_pid = os.getpid()
    current_script = os.path.basename(sys.argv[0]).lower()

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.pid == current_pid:
                continue

            if proc.info['cmdline'] and len(proc.info['cmdline']) > 0:
                script_name = os.path.basename(proc.info['cmdline'][0]).lower()
                if script_name == current_script and 'python' in proc.info['name'].lower():
                    print(f"Killing duplicate process PID: {proc.pid}")
                    proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, IndexError):
            continue

if __name__ == "__main__":
    kill_other_instances()
    start_listener()
    print("Service running. Press Ctrl+F13 to improve text. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        if listener:
            listener.stop()
        sys.exit(0)