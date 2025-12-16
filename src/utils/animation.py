"""
Loading animation utilities
Provides animated progress indicators for terminal
"""

import sys
import time
import threading
import random
import contextlib
from src.utils.colors import ColorText


class LoadingAnimation:
    """Class for handling loading animations in terminal with smooth effects"""

    def __init__(self, description: str = "Processing"):
        self.description = description
        self.is_running = False
        self.animation_thread = None
        self.progress = 0
        self.animations = {
            "smooth_bar": [
                "▰▱▱▱▱▱▱▱▱▱",
                "▰▰▱▱▱▱▱▱▱▱",
                "▰▰▰▱▱▱▱▱▱▱",
                "▰▰▰▰▱▱▱▱▱▱",
                "▰▰▰▰▰▱▱▱▱▱",
                "▰▰▰▰▰▰▱▱▱▱",
                "▰▰▰▰▰▰▰▱▱▱",
                "▰▰▰▰▰▰▰▰▱▱",
                "▰▰▰▰▰▰▰▰▰▱",
                "▰▰▰▰▰▰▰▰▰▰",
            ],
            "wave": ["≋", "≈", "≋", "≈", "≋"],
            "spinner": ["◜", "◠", "◝", "◞", "◡", "◟"],
            "pulse": ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"],
        }
        self.colors = [
            ColorText.BLUE,
            ColorText.CYAN,
            ColorText.GREEN,
            ColorText.YELLOW,
        ]
        self.current_color = random.choice(self.colors)
        self.animation_chars = self.animations["smooth_bar"]

    def start(self):
        """Start loading animation"""
        self.is_running = True
        self.animation_thread = threading.Thread(target=self._animate)
        self.animation_thread.daemon = True
        self.animation_thread.start()

    def stop(self):
        """Stop loading animation"""
        self.is_running = False
        if self.animation_thread:
            self.animation_thread.join()
        sys.stdout.write("\r" + " " * (len(self.description) + 30) + "\r")
        sys.stdout.flush()

    def _animate(self):
        """Internal function to run animation with smooth effects"""
        while self.is_running:
            for frame in self.animation_chars:
                if not self.is_running:
                    break
                animation = f"{self.current_color}{frame}{ColorText.END}"
                sys.stdout.write(f"\r{animation} {self.description} ")
                sys.stdout.flush()
                time.sleep(0.1)


@contextlib.contextmanager
def loading_animation(description: str = "Processing"):
    """Context manager for loading animation"""
    spinner = LoadingAnimation(description)
    spinner.start()
    try:
        yield spinner
    finally:
        spinner.stop()