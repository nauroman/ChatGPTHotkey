﻿#!/usr/bin/env python3

import os
import sys
import time
import threading
import logging
from typing import Optional
import subprocess

import pyautogui
import pyperclip
from pynput import keyboard
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


# Singleton pattern to ensure only one instance runs
class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
            return cls._instances[cls]


# Main application class
class TextImprover(metaclass=SingletonMeta):
    def __init__(self):
        self.settings = {
            "api_key": os.environ.get("OPENAI_API_KEY"),
            "model": "gpt-4o-mini",
            "hotkey": "<ctrl>+<f13>",
            "prompt": """The GPT's role is to correct texts to reflect educated polite American English, 
                        adjusting grammar, syntax, and idioms while preserving meaning. 
                        Translate into English if necessary. It should maintain clarity, accuracy, 
                        and a neutral tone, avoiding unnecessary changes or complex vocabulary. 
                        The GPT should not ask for clarification; it should simply provide the 
                        corrected text without any introductions or additions such as 
                        'here is the improved version.' Text to correct:"""
        }

        # Validate API key
        if not self.settings["api_key"]:
            logger.error("OPENAI_API_KEY environment variable not set")
            sys.exit(1)

        self.client = OpenAI(api_key=self.settings["api_key"])
        self.running = True
        self.hotkey_listener = None

        # Install dependencies if needed
        self._install_dependencies()

        # Start the hotkey listener
        self._start_listener()

    def _install_dependencies(self) -> None:
        """Install required Python packages if not already installed."""
        dependencies = ["pyautogui", "pyperclip", "pynput", "openai"]

        for package in dependencies:
            try:
                __import__(package)
            except ImportError:
                logger.info(f"Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                logger.info(f"{package} installed successfully")

    def improve_text(self, text: str) -> str:
        """Call OpenAI API to improve the selected text."""
        prompt = f"{self.settings['prompt'].strip()}\n\n{text}"

        try:
            logger.info("Calling OpenAI API...")
            completion = self.client.chat.completions.create(
                model=self.settings["model"],
                messages=[{"role": "user", "content": prompt}]
            )
            improved_text = completion.choices[0].message.content.strip()
            logger.info("Text improved successfully")
            return improved_text
        except Exception as e:
            logger.error(f"OpenAI API Error: {e}")
            return text

    def _process_hotkey(self) -> None:
        """Handle the hotkey press event."""
        try:
            logger.info("Hotkey triggered")

            # Simulate Ctrl+A and Ctrl+C
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)  # Small delay to ensure selection
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.1)  # Small delay to ensure copy

            # Get text from clipboard
            selected_text = pyperclip.paste()
            if not selected_text:
                logger.warning("No text selected")
                return

            logger.info(f"Selected text: {selected_text[:50]}...")

            # Improve text via API
            improved_text = self.improve_text(selected_text)

            # Update clipboard and paste
            pyperclip.copy(improved_text)
            pyautogui.hotkey('ctrl', 'v')
            logger.info("Improved text pasted successfully")

        except Exception as e:
            logger.error(f"Error processing hotkey: {e}")

    def _on_hotkey(self) -> None:
        """Callback for hotkey press."""
        # Run processing in a separate thread to avoid blocking
        threading.Thread(target=self._process_hotkey, daemon=True).start()

    def _start_listener(self) -> None:
        """Start the keyboard listener."""
        try:
            # Convert hotkey string to pynput format
            hotkey_combo = keyboard.HotKey(
                keyboard.HotKey.parse(self.settings["hotkey"]),
                self._on_hotkey
            )

            def for_canonical(f):
                return lambda k: f(listener.canonical(k))

            listener = keyboard.Listener(
                on_press=for_canonical(hotkey_combo.press),
                on_release=for_canonical(hotkey_combo.release)
            )
            self.hotkey_listener = listener
            listener.start()
            logger.info(f"Listening for hotkey: {self.settings['hotkey']}")

        except Exception as e:
            logger.error(f"Failed to start listener: {e}")
            sys.exit(1)

    def run(self) -> None:
        """Keep the application running."""
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            self.running = False


def check_single_instance() -> bool:
    """Check if another instance is already running."""
    import psutil

    current_pid = os.getpid()
    script_name = os.path.basename(__file__)
    instances = 0

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.pid != current_pid and script_name in ' '.join(proc.info['cmdline'] or []):
                instances += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return instances == 0


def main():
    """Main entry point."""
    if not check_single_instance():
        logger.error("Another instance is already running")
        sys.exit(1)

    logger.info("Starting Text Improver...")
    app = TextImprover()
    app.run()

if __name__ == "__main__":
    main()