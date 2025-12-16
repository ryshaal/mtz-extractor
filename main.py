"""
MTZ Tool - Extract and Pack MTZ files
Main entry point for the application
"""

import os
import sys
from src.ui.menu import MainMenu  # ← Ubah ini! Hapus angka 1
from src.utils.terminal import clear_screen


def main():
    """Main function to run the application"""
    try:
        clear_screen()
        menu = MainMenu()
        menu.run()
    except KeyboardInterrupt:
        clear_screen()
        print("\n⚠️ Application terminated by user\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()