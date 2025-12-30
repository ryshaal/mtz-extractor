# MTZ Extractor - Xiaomi MIUI Themes Extractor
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-3.0-brightgreen.svg)

This repository contains a Python tool for **extracting** and **packing** `.mtz` files, specifically designed for Xiaomi MIUI themes. The tool allows easy access to the contents of `.mtz` theme files and enables you to create your own MTZ packages, making theme customization and modification much simpler.

In addition, a desktop application version is also available — a Python-based app for extracting, compressing, and managing MIUI theme files (`.mtz`). It is built using **CustomTkinter**, featuring a modern graphical interface with **drag-and-drop** support.

[![Download](https://img.shields.io/badge/Download%20MTZ_Extractor-v2.0-blue?style=for-the-badge&logo=windows)](https://github.com/ryshaal/mtz_extractor/releases/download/v2.0/MTZ_Extractor.exe)

<a href='https://ko-fi.com/riyhsal/5' target='_blank'><img height='40' style='border:0px;height:40px;' src='https://storage.ko-fi.com/cdn/kofi2.png?v=6' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

## Features

- **Extract MTZ Files**: Decompress MTZ theme files into organized folders with automatic nested archive handling
- **Pack to MTZ**: Compress folders into MTZ theme files with smart compression
- **Beautiful Terminal UI**: Colorful interface with smooth loading animations
- **Detailed Logging**: Automatic logging of operations with system information
- **Smart Processing**: 
  - Automatic handling of nested archives and file structures
  - Skip unnecessary files (wallpaper, preview folders)
  - Empty folder cleanup
  - Full path display for easy access
- **Statistics Dashboard**: Detailed statistics for compression ratios, file counts, and processing time
- **Cross-Platform**: Works on Windows, Linux, and macOS

## Requirements

This tool requires **Python 3.7 or higher** to run. Ensure you have the necessary Python version installed on your system.

### Install Dependencies

This project uses Python's built-in modules, plus one additional `psutil` module. Run the following command to install dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install psutil
```

## Installation & Usage

### 1. Clone the repository

```bash
git clone https://github.com/ryshaal/mtz_extractor.git
cd mtz_extractor
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the tool

```bash
python main.py
```

## How to Use

### Main Menu

When you run the tool, you'll see an interactive menu with 3 options:

```
╔═════════════════════════════════════╗
║          MTZ Tool v3.0              ║
║     Extract & Pack MTZ Files        ║
║           BY Ryhshall               ║
╚═════════════════════════════════════╝

📋 Menu Options:
  1. Extract MTZ File
  2. Pack to MTZ File
  3. Exit

➤ Choose option (1-3): 
```

### Option 1: Extract MTZ File

1. Select option `1` from the menu
2. Enter the full path to your `.mtz` file
3. The tool will:
   - Extract the MTZ file
   - Process nested archives automatically
   - Clean up empty folders
   - Display extraction statistics
4. Files will be extracted to `./extracted/[theme_name]/` folder
5. Full absolute path will be displayed for easy access

**Example:**
```
📂 Enter MTZ file location: D:\Themes\MyTheme.mtz

⏳ Starting extraction process...

✨ Extraction Successful! ✨

📊 Extraction Statistics:
├─ Total files: 245
├─ Original size: 15.67 MB
├─ Final size: 45.23 MB
├─ Expansion ratio: 288.7%
├─ Processing time: 3.2 seconds
└─ Location: D:\mtz-tool\extracted\MyTheme
```

### Option 2: Pack to MTZ File

1. Select option `2` from the menu
2. Enter the full path to the folder you want to pack
3. The tool will:
   - Compress all subfolders (except wallpaper/preview)
   - Verify ZIP integrity
   - Create the final MTZ file
   - Display packing statistics
4. MTZ file will be created in the same directory as the source folder
5. Original folder will be removed after successful packing

**Example:**
```
📂 Enter folder location to pack: D:\extracted\MyTheme

⏳ Starting packing process...

✓ Compressed: icons (1/5)
✓ Compressed: lockscreen (2/5)
✓ Compressed: framework-res (3/5)
...

✨ Packing Successful! ✨

📊 Packing Statistics:
├─ Total files: 245
├─ Original size: 45.23 MB
├─ Final size: 15.67 MB
├─ Compression ratio: 34.6%
├─ Processing time: 5.8 seconds
└─ MTZ file: D:\extracted\MyTheme.mtz
```

### Option 3: Exit

Select option `3` to exit the application safely.

## Project Structure

```
mtz-extractor/
│
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License
├── .gitignore            # Git ignore rules
│
├── src/
│   ├── __init__.py
│   │
│   ├── core/              # Core functionality
│   │   ├── __init__.py
│   │   ├── extractor.py   # MTZ extraction logic
│   │   └── compressor.py  # MTZ packing logic
│   │
│   ├── ui/                # User interface
│   │   ├── __init__.py
│   │   └── menu.py        # Main menu and navigation
│   │
│   └── utils/             # Utility modules
│       ├── __init__.py
│       ├── colors.py      # Terminal color utilities
│       ├── animation.py   # Loading animations
│       ├── logger.py      # Logging configuration
│       └── terminal.py    # Terminal helper functions
│
├── logs/                  # Log files (auto-generated)
└── extracted/             # Extracted files (auto-generated)
```

## Features in Detail

### Color-Coded Output
- **Cyan**: Information and prompts
- **Green**: Success messages and checkmarks
- **Yellow**: Highlights and important information
- **Red**: Errors and warnings

### Smart Loading Animations
Beautiful animated progress indicators during:
- File extraction
- Compression operations
- ZIP verification
- File processing
- MTZ creation

### Automatic Logging
Every operation is logged with:
- Timestamp and duration
- System information (OS, CPU, Memory)
- Operation details and file counts
- Error tracking and debugging info
- Full paths for easy reference

Logs are saved in `./logs/` folder with timestamps.

### Smart File Handling
- **Automatic nested archive extraction**: Handles ZIP files within MTZ
- **Folder structure preservation**: Maintains original hierarchy
- **Selective processing**: Skips wallpaper and preview folders during packing
- **Empty folder cleanup**: Removes unnecessary empty directories
- **Duplicate handling**: Creates numbered copies if folder exists

## Statistics Dashboard

After each operation, you'll see detailed statistics:
- **Total files processed**: Number of files handled
- **Original size**: Size before operation
- **Final size**: Size after operation
- **Compression/Expansion ratio**: Percentage change
- **Processing time**: Duration in seconds
- **Output location**: Full absolute path

## Development

### Adding New Features

1. Core functionality goes in `src/core/`
2. UI components go in `src/ui/`
3. Utility functions go in `src/utils/`

### Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions focused and modular

## Troubleshooting

### Common Issues

**Import Error**: 
- Make sure you're in the project root directory
- Ensure all dependencies are installed: `pip install -r requirements.txt`

**Permission Error**: 
- Ensure you have read/write permissions for target directories
- Run as administrator on Windows if needed

**Memory Error**: 
- Large MTZ files may require significant RAM
- Close other applications to free up memory
- Process smaller themes if issues persist

**Path Not Found**:
- Use absolute paths for reliability
- Ensure file/folder exists before processing
- Check for special characters in path names

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.



## Show your support

Give a ⭐️ if this project helped you!

<a href='https://ko-fi.com/riyhsal' target='_blank'><img height='40' style='border:0px;height:40px;' src='https://storage.ko-fi.com/cdn/kofi2.png?v=6' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

## Contact

For questions or suggestions, please open an issue on GitHub.

