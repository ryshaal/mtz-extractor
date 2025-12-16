"""
Color utilities for terminal output
Provides ANSI color codes for styling text
"""


class ColorText:
    """Class for handling text colors in terminal"""

    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    @staticmethod
    def blue(text: str) -> str:
        """Return text in blue color"""
        return f"{ColorText.BLUE}{text}{ColorText.END}"

    @staticmethod
    def green(text: str) -> str:
        """Return text in green color"""
        return f"{ColorText.GREEN}{text}{ColorText.END}"

    @staticmethod
    def red(text: str) -> str:
        """Return text in red color"""
        return f"{ColorText.RED}{text}{ColorText.END}"

    @staticmethod
    def yellow(text: str) -> str:
        """Return text in yellow color"""
        return f"{ColorText.YELLOW}{text}{ColorText.END}"

    @staticmethod
    def cyan(text: str) -> str:
        """Return text in cyan color"""
        return f"{ColorText.CYAN}{text}{ColorText.END}"

    @staticmethod
    def bold(text: str) -> str:
        """Return text in bold"""
        return f"{ColorText.BOLD}{text}{ColorText.END}"