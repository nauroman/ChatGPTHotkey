#!/usr/bin/env python3
import subprocess
import sys
import importlib.util

dependencies = ["pyperclip", "pynput", "openai", "psutil"]

for dep in dependencies:
    if importlib.util.find_spec(dep) is None:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
        print(f"{dep} installed successfully")

# Now import the required modules
import os
import time
import threading
import logging
from typing import Optional
import argparse

import pyperclip
from pynput import keyboard
from openai import OpenAI
import ctypes

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
    def __init__(self, api_key: str = None, hotkey: str = None, model: str = None, prompt: str = None):
        # Default settings
        self.settings = {
            "api_key": os.environ.get("OPENAI_API_KEY"),
            "model": "gpt-4.1-nano",
            "hotkey": "<ctrl>+<f13>",
            "prompt": """The GPT's role is to correct texts to reflect educated polite American English, 
                        adjusting grammar, syntax, and idioms while preserving meaning. 
                        Translate into English if necessary. It should maintain clarity, accuracy, 
                        and a neutral tone, avoiding unnecessary changes or complex vocabulary. 
                        The GPT should not ask for clarification; it should simply provide the 
                        corrected text without any introductions or additions such as 
                        'here is the improved version.' Text to correct:"""
        }

        # Override defaults with command-line arguments if provided
        if api_key:
            self.settings["api_key"] = api_key
        if hotkey:
            self.settings["hotkey"] = hotkey
        if model:
            self.settings["model"] = model
        if prompt:
            self.settings["prompt"] = prompt

        # Validate API key
        if not self.settings["api_key"]:
            logger.error("API key not provided via argument or OPENAI_API_KEY environment variable")
            sys.exit(1)

        self.client = OpenAI(api_key=self.settings["api_key"])
        self.running = True
        self.processing_lock = threading.Lock()

        # Start the hotkey listener
        self._start_listener()

    # Windows virtual key codes
    VK_CONTROL = 0x11
    VK_A = 0x41
    VK_C = 0x43
    VK_V = 0x56
    KEYEVENTF_KEYUP = 0x0002

    def _send_key_combo(self, vk_key: int):
        """Send Ctrl+Key combination using ctypes and Win32 API."""
        ctypes.windll.user32.keybd_event(self.VK_CONTROL, 0, 0, 0)
        ctypes.windll.user32.keybd_event(vk_key, 0, 0, 0)
        ctypes.windll.user32.keybd_event(vk_key, 0, self.KEYEVENTF_KEYUP, 0)
        ctypes.windll.user32.keybd_event(self.VK_CONTROL, 0, self.KEYEVENTF_KEYUP, 0)

    def _send_ctrl_a(self):
        """Send Ctrl+A using ctypes and Win32 API."""
        self._send_key_combo(self.VK_A)

    def _send_ctrl_c(self):
        """Send Ctrl+C using ctypes and Win32 API."""
        self._send_key_combo(self.VK_C)

    def _send_ctrl_v(self):
        """Send Ctrl+V using ctypes and Win32 API."""
        self._send_key_combo(self.VK_V)

    def _capture_selected_text(self) -> Optional[str]:
        """Attempt to copy currently selected text, restoring the clipboard on failure."""
        original_clipboard = pyperclip.paste()

        try:
            # Clear clipboard first
            pyperclip.copy("")
            time.sleep(0.05)

            self._send_ctrl_a()
            time.sleep(0.05)
            self._send_ctrl_c()
            time.sleep(0.15)

            for attempt in range(3):
                try:
                    selected_text = pyperclip.paste()
                    if selected_text and selected_text.strip():
                        return selected_text
                except Exception as exc:
                    logger.error(f"Failed to read clipboard: {exc}")

                if attempt < 2:
                    self._send_ctrl_a()
                    time.sleep(0.05)
                    self._send_ctrl_c()
                    time.sleep(0.15)

            logger.warning("No text selected")
            pyperclip.copy(original_clipboard)
            return None

        except Exception as exc:
            logger.error(f"Failed during selection capture: {exc}")
            pyperclip.copy(original_clipboard)
            return None

    def improve_text(self, text: str) -> str:
        """Call OpenAI API to improve the selected text."""
        prompt = f"{self.settings['prompt'].strip()}\n\n{text}"

        try:
            logger.info(f"Calling OpenAI API (model: {self.settings['model']})...")
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
        if not self.processing_lock.acquire(blocking=False):
            logger.warning("Processing already in progress; ignoring hotkey trigger")
            return

        try:
            logger.info("Hotkey triggered")

            selected_text = self._capture_selected_text()
            if not selected_text:
                return

            logger.info(f"Selected text: {selected_text[:50]}...")

            # Improve text via API
            improved_text = self.improve_text(selected_text)

            # Update clipboard and paste
            pyperclip.copy(improved_text)
            time.sleep(0.05)
            self._send_ctrl_v()
            logger.info("Improved text pasted successfully")

        except Exception as e:
            logger.error(f"Error processing hotkey: {e}")
        finally:
            self.processing_lock.release()

    def _on_hotkey(self) -> None:
        """Callback for hotkey press."""
        # Run processing in a separate thread to avoid blocking
        threading.Thread(target=self._process_hotkey, daemon=True).start()

    def _start_listener(self) -> None:
        """Start the keyboard listener."""
        try:
            hotkey_combo = keyboard.HotKey(
                keyboard.HotKey.parse(self.settings["hotkey"]),
                self._on_hotkey
            )

            listener = keyboard.Listener(
                on_press=lambda k: hotkey_combo.press(listener.canonical(k)),
                on_release=lambda k: hotkey_combo.release(listener.canonical(k))
            )
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

    for proc in psutil.process_iter(['pid', 'cmdline']):
        try:
            if proc.pid != current_pid and script_name in ' '.join(proc.info['cmdline'] or []):
                return False
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return True

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Text Improver Hotkey Script")
    parser.add_argument("--api_key", help="OpenAI API key")
    parser.add_argument("--hotkey", help="Hotkey to trigger the script (e.g., '<ctrl>+<f13>')")
    parser.add_argument("--model", help="OpenAI model to use (e.g., 'gpt-4.1-nano')")
    parser.add_argument("--prompt", help="Prompt for the OpenAI model")
    return parser.parse_args()

def main():
    """Main entry point."""
    if not check_single_instance():
        logger.error("Another instance is already running")
        sys.exit(1)

    # Parse command-line arguments
    args = parse_args()

    logger.info("Starting Text Improver...")
    app = TextImprover(
        api_key=args.api_key,
        hotkey=args.hotkey,
        model=args.model,
        prompt=args.prompt
    )
    app.run()

if __name__ == "__main__":
    main()