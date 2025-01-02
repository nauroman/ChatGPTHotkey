import sys
import subprocess

# Attempt to install required packages if not present
required_packages = ["openai", "keyboard", "pyperclip", "pyautogui", "os", "argparse"]
for pkg in required_packages:
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

import keyboard
import pyperclip
import pyautogui
import os
import argparse
from openai import OpenAI

settings = {"api_key": os.environ.get("OPENAI_API_KEY"), "model": "gpt-4o-mini", "hotkey": "ctrl+f11",
            "prompt": "The GPT's role is to correct texts to reflect educated polite American English, adjusting grammar, syntax, and idioms while preserving meaning. Translate into English if necessary. It should maintain clarity, accuracy, and a neutral tone, avoiding unnecessary changes or complex vocabulary. The GPT should not ask for clarification; it should simply provide the updated text without any introductions or additions such as 'here is the improved version.' Text to correct :"}

client = OpenAI()


def improve_text(text: str) -> str:
    prompt = (settings["prompt"].strip()) + f"\n\n{text}"

    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt}
                    ],
                }
            ],
            model=settings["model"],
        )
        improved_text = completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        improved_text = text  # Return the original text in case of error
    return improved_text


def on_hotkey():
    # Copy currently selected text
    pyautogui.hotkey("ctrl", "a")
    pyautogui.sleep(0.2)  # small delay to ensure clipboard updates
    pyautogui.hotkey("ctrl", "c")
    pyautogui.sleep(0.2)  # small delay to ensure clipboard updates
    text = pyperclip.paste()
    if not text:
        return  # No text found in clipboard

    improved = improve_text(text)

    pyperclip.copy(improved)
    pyautogui.hotkey("ctrl", "v")


def load_settings_from_file():
    if os.path.exists("settings.txt"):
        with open("settings.txt", "r") as f:
            for line in f:
                key, value = line.strip().split("=")
                if value.strip():
                    settings[key] = value


def get_arguments():
    parser = argparse.ArgumentParser(description="Load settings for the script.")
    parser.add_argument("--api_key", type=str, help="OpenAI API key", required=False, default=settings["api_key"])
    parser.add_argument("--hotkey", type=str, help="Hotkey to trigger the script", required=False,
                        default=settings["hotkey"])
    parser.add_argument("--model", type=str, help="OpenAI model to use", required=False, default=settings["model"])
    parser.add_argument("--prompt", type=str, help="Prompt for the OpenAI model", required=False,
                        default=settings["prompt"])

    args = parser.parse_args()

    settings["api_key"] = args.api_key if args.api_key and "openai_api_key" not in args.api_key else settings["api_key"]
    settings["hotkey"] = args.hotkey if args.hotkey else settings["hotkey"]
    settings["model"] = args.model if args.model else settings["model"]
    settings["prompt"] = args.prompt if args.prompt else settings["prompt"]

    settings["api_key"] = settings["api_key"].strip()
    settings["hotkey"] = settings["hotkey"].strip()
    settings["model"] = settings["model"].strip()
    settings["prompt"] = settings["prompt"].strip()


def start_keyboard():
    if settings["hotkey"]:
        try:
            keyboard.add_hotkey(settings["hotkey"], on_hotkey)
            print(f"Script is running in the background. Press the hotkey {settings["hotkey"]} to improve the text.")
        except Exception as e:
            print(f"Error setting hotkey: {e}")
            pass
    keyboard.wait("esc")


def main():
    load_settings_from_file()
    get_arguments()
    client.api_key = settings["api_key"]

    try:
        start_keyboard()
    except KeyboardInterrupt:
        print("\nScript terminated by user.")


if __name__ == '__main__':
    main()
