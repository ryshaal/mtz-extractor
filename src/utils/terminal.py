"""
Terminal utilities
Provides helper functions for terminal operations
"""

import os


def clear_screen():
    """Clear terminal screen based on operating system"""
    os.system("cls" if os.name == "nt" else "clear")