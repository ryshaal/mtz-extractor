"""
MTZ Extractor module
Handles extraction of MTZ files
"""

import os
import sys
import zipfile
import time
from typing import Set, Optional
from pathlib import Path
from src.utils.colors import ColorText
from src.utils.animation import loading_animation
from src.utils.logger import setup_logger


class MTZExtractor:
    """Class for handling MTZ file extraction"""

    def __init__(self, allowed_extensions: Set[str] = None):
        self.allowed_extensions = allowed_extensions or {
            ".java", ".kt", ".so", ".aar", ".jar", ".mp3", ".wav",
            ".mp4", ".3gp", ".txt", ".json", ".xml", ".html", ".css",
            ".js", ".ttf", ".otf", ".png", ".jpg", ".jpeg", ".gif",
            ".webp", ".pdf", ".gradle", ".properties", ".MF", ".SF",
            ".RSA",
        }
        self.logger = setup_logger("MTZExtractor")
        self.stats = {
            "start_time": None,
            "total_files": 0,
            "total_size": 0,
            "extracted_size": 0,
        }

    def print_banner(self):
        """Display application banner"""
        banner = f"""
{ColorText.cyan('╔═══════════════════════════════════════╗')}
{ColorText.cyan('║')}           {ColorText.bold('MTZ Tool v3.0')}               {ColorText.cyan('║')}
{ColorText.cyan('║')}      {ColorText.yellow('Extract & Pack MTZ Files')}         {ColorText.cyan('║')}
{ColorText.cyan('║')}            {ColorText.cyan('BY Ryhshall')}                {ColorText.cyan('║')}
{ColorText.cyan('╚═══════════════════════════════════════╝')}
"""
        print(banner)

    def format_size(self, size: int) -> str:
        """Format file size in readable format"""
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"

    def validate_mtz_file(self, file_path: str) -> bool:
        """Validate if file is MTZ"""
        if not os.path.exists(file_path):
            print(f"\n{ColorText.red('❌ File not found!')}")
            return False

        if not file_path.endswith(".mtz"):
            print(f"\n{ColorText.red('❌ File is not MTZ format!')}")
            return False

        return True

    def create_extract_folder(self, file_path: str) -> Optional[str]:
        """Create unique extraction folder"""
        try:
            file_name = Path(file_path).stem
            base_extract_folder = Path("./extracted")
            extract_folder = base_extract_folder / file_name

            counter = 1
            while extract_folder.exists():
                extract_folder = base_extract_folder / f"{file_name}_copy{counter}"
                counter += 1

            extract_folder.mkdir(parents=True, exist_ok=True)
            
            # Get absolute path for logging
            absolute_path = os.path.abspath(str(extract_folder))
            self.logger.info(f"Created extraction folder: {absolute_path}")
            
            return str(extract_folder)

        except Exception as e:
            print(f"\n{ColorText.red(f'❌ Failed to create folder: {str(e)}')}")
            self.logger.error(f"Failed to create folder: {str(e)}")
            return None

    def extract_mtz(self, file_path: str, extract_folder: str) -> bool:
        """Extract MTZ file to folder"""
        try:
            self.stats["start_time"] = time.time()
            self.stats["total_size"] = os.path.getsize(file_path)

            with loading_animation(
                f"Extracting {ColorText.yellow(os.path.basename(file_path))} "
                f"({self.format_size(self.stats['total_size'])})"
            ):
                with zipfile.ZipFile(file_path, "r") as zip_ref:
                    zip_ref.extractall(extract_folder)
                    self.stats["total_files"] = len(zip_ref.namelist())
            
            self.logger.info(f"Extracted {self.stats['total_files']} files")
            return True
        except Exception as e:
            print(f"\n{ColorText.red(f'❌ Extraction failed: {str(e)}')}")
            self.logger.error(f"Extraction failed: {str(e)}")
            return False

    def process_files(self, folder: str) -> None:
        """Process files after extraction"""
        with loading_animation(f"Processing {ColorText.yellow(os.path.basename(folder))}"):
            self._add_zip_extension_to_files(folder)
            self._unzip_files_to_folders(folder)
            self._cleanup_empty_folders(folder)
            self.stats["extracted_size"] = self.calculate_folder_size(folder)
        
        self.logger.info("File processing completed")

    def calculate_folder_size(self, folder: str) -> int:
        """Calculate total folder size"""
        total_size = 0
        for dirpath, _, filenames in os.walk(folder):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    def _add_zip_extension_to_files(self, folder: str) -> None:
        """Add .zip extension to files that are not allowed extensions"""
        for file_path in Path(folder).rglob("*"):
            if file_path.is_file() and file_path.suffix not in self.allowed_extensions:
                new_path = file_path.with_suffix(file_path.suffix + ".zip")
                file_path.rename(new_path)
                self.logger.debug(f"Renamed: {file_path} to {new_path}")

    def _unzip_files_to_folders(self, folder: str) -> None:
        """Extract .zip files to their respective folders"""
        for file_path in Path(folder).rglob("*.zip"):
            if file_path.is_file():
                folder_path = file_path.with_suffix("")
                folder_path.mkdir(exist_ok=True)

                try:
                    with zipfile.ZipFile(file_path, "r") as zip_ref:
                        zip_ref.extractall(folder_path)
                    file_path.unlink()
                    self.logger.debug(f"Extracted and removed: {file_path}")
                except Exception as e:
                    self.logger.warning(f"Failed to extract {file_path}: {str(e)}")
                    continue

    def _cleanup_empty_folders(self, folder: str) -> None:
        """Remove empty folders"""
        for dirpath, dirnames, filenames in os.walk(folder, topdown=False):
            if not dirnames and not filenames:
                try:
                    os.rmdir(dirpath)
                    self.logger.debug(f"Removed empty folder: {dirpath}")
                except OSError:
                    continue

    def show_completion(self, extract_folder: str):
        """Display completion message with statistics"""
        completion_time = time.time() - self.stats["start_time"]
        expansion_ratio = (
            (self.stats["extracted_size"] / self.stats["total_size"]) * 100
            if self.stats["total_size"] > 0
            else 0
        )

        # Get absolute path
        absolute_path = os.path.abspath(extract_folder)

        print(f"\n{ColorText.green('✨ Extraction Successful! ✨')}")
        print(f"\n{ColorText.cyan('📊 Extraction Statistics:')}")
        print(f"├─ Total files: {ColorText.yellow(str(self.stats['total_files']))}")
        print(
            f"├─ Original size: {ColorText.yellow(self.format_size(self.stats['total_size']))}"
        )
        print(
            f"├─ Final size: {ColorText.yellow(self.format_size(self.stats['extracted_size']))}"
        )
        print(f"├─ Expansion ratio: {ColorText.yellow(f'{expansion_ratio:.1f}%')}")
        print(f"├─ Processing time: {ColorText.yellow(f'{completion_time:.1f} seconds')}")
        print(f"└─ Location: {ColorText.yellow(absolute_path)}\n")
        
        self.logger.info(f"Extraction completed in {completion_time:.1f} seconds")
        self.logger.info(f"Extracted to: {absolute_path}")