"""
MTZ Compressor module
Handles packing of folders into MTZ files
"""

import os
import zipfile
import shutil
import time
from typing import Optional
from pathlib import Path
from src.utils.colors import ColorText
from src.utils.animation import loading_animation
from src.utils.logger import setup_logger


class MTZCompressor:
    """Class for handling MTZ file compression"""

    def __init__(self):
        self.logger = setup_logger("MTZCompressor")
        self.stats = {
            "start_time": None,
            "total_files": 0,
            "total_size": 0,
            "compressed_size": 0,
        }

    def print_banner(self):
        """Display application banner"""
        banner = f"""
{ColorText.cyan('╔═══════════════════════════════════════╗')}
{ColorText.cyan('║')}           {ColorText.bold('MTZ Tool v3.0')}               {ColorText.cyan('║')}
{ColorText.cyan('║')}      {ColorText.yellow('Extract & Pack MTZ Files')}         {ColorText.cyan('║')}
{ColorText.cyan('║')}            {ColorText.cyan('BY Ryhshall')}                {ColorText.cyan('║')}
{ColorText.cyan('╚═══════════════════════════════════════╝')}"""
        print(banner)

    def validate_folder(self, folder_path: str) -> bool:
        """Validate if folder exists and is a directory"""
        if not os.path.exists(folder_path):
            print(f"\n{ColorText.red('❌ Folder not found!')}")
            return False

        if not os.path.isdir(folder_path):
            print(f"\n{ColorText.red('❌ Path is not a folder!')}")
            return False

        return True

    def calculate_size(self, path: str) -> int:
        """Calculate folder/file size"""
        if os.path.isfile(path):
            return os.path.getsize(path)
        total = 0
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total += os.path.getsize(fp)
        return total

    def format_size(self, size: int) -> str:
        """Format file size in readable format"""
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"

    def zip_folder(self, folder_path: str) -> Optional[str]:
        """Compress folder to ZIP"""
        try:
            folder_size = self.calculate_size(folder_path)
            with loading_animation(
                f"Compressing {ColorText.yellow(os.path.basename(folder_path))} "
                f"({self.format_size(folder_size)})"
            ):
                zip_path = f"{folder_path}.zip"
                with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_STORED) as zipf:
                    for root, dirs, files in os.walk(folder_path):
                        if os.path.basename(root) in ["wallpaper", "preview"]:
                            continue

                        if not files and not dirs:
                            arcname = os.path.relpath(root, folder_path) + "/"
                            zipf.write(root, arcname)
                        else:
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, folder_path)
                                zipf.write(file_path, arcname)
                                self.stats["total_files"] += 1
                                self.stats["total_size"] += os.path.getsize(file_path)

            self.logger.info(f"Compressed folder: {folder_path}")
            return zip_path
        except Exception as e:
            self.logger.error(f"Error compressing folder: {str(e)}")
            return None

    def verify_zip(self, zip_path: str) -> bool:
        """Verify ZIP file integrity"""
        with loading_animation(
            f"Verifying {ColorText.yellow(os.path.basename(zip_path))}"
        ):
            try:
                with zipfile.ZipFile(zip_path, "r") as zipf:
                    corrupt_file = zipf.testzip()
                    if corrupt_file is not None:
                        self.logger.error(f"Corrupt file: {corrupt_file}")
                        return False
                    return True
            except Exception as e:
                self.logger.error(f"Error verifying ZIP: {str(e)}")
                return False

    def remove_zip_extension(self, folder_path: str) -> None:
        """Remove .zip extension from files"""
        with loading_animation(
            f"Removing ZIP extensions from {ColorText.yellow(os.path.basename(folder_path))}"
        ):
            try:
                folder_path = os.path.abspath(folder_path)
                for filename in os.listdir(folder_path):
                    if filename.endswith(".zip"):
                        old_path = os.path.join(folder_path, filename)
                        new_path = os.path.join(folder_path, filename[:-4])
                        os.rename(old_path, new_path)
                        self.logger.info(f"Renamed: {old_path} to {new_path}")
            except Exception as e:
                self.logger.error(f"Error removing ZIP extensions: {str(e)}")

    def create_mtz(self, folder_path: str) -> bool:
        """Create MTZ file from folder"""
        with loading_animation(f"Creating {ColorText.yellow('MTZ')} file"):
            try:
                folder_path = os.path.abspath(folder_path)
                mtz_path = folder_path + ".mtz"

                with zipfile.ZipFile(mtz_path, "w", zipfile.ZIP_DEFLATED) as zf:
                    for root, dirs, files in os.walk(folder_path):
                        for file in files:
                            full_path = os.path.join(root, file)
                            rel_path = os.path.relpath(full_path, folder_path)
                            zf.write(full_path, rel_path)
                            self.logger.debug(f"Added to MTZ: {rel_path}")

                if os.path.exists(mtz_path):
                    self.stats["compressed_size"] = os.path.getsize(mtz_path)
                    shutil.rmtree(folder_path)
                    self.logger.info(f"MTZ file created: {mtz_path}")
                    return True
                return False
            except Exception as e:
                self.logger.error(f"Error creating MTZ: {str(e)}")
                return False

    def pack_to_mtz(self, main_folder: str) -> bool:
        """Main function to pack folder to MTZ"""
        try:
            self.stats["start_time"] = time.time()

            # Step 1: Compress folders to ZIP
            for folder in os.listdir(main_folder):
                folder_path = os.path.join(main_folder, folder)

                if folder in ["wallpaper", "preview"]:
                    self.logger.info(f"Skipping folder: {folder}")
                    continue

                if os.path.isdir(folder_path):
                    zip_path = self.zip_folder(folder_path)
                    if zip_path and self.verify_zip(zip_path):
                        shutil.rmtree(folder_path)
                        print(f"{ColorText.green('✓')} {folder}")
                        self.logger.info(f"Folder successfully compressed: {folder}")

            # Step 2: Remove ZIP extensions
            self.remove_zip_extension(main_folder)

            # Step 3: Create MTZ file
            return self.create_mtz(main_folder)

        except Exception as e:
            self.logger.error(f"Error in pack_to_mtz: {str(e)}")
            return False

    def show_completion(self, folder_path: str):
        """Display completion message with statistics"""
        mtz_path = folder_path + ".mtz"
        
        # Get absolute path
        absolute_mtz_path = os.path.abspath(mtz_path)

        completion_time = time.time() - self.stats["start_time"]
        compression_ratio = (
            (self.stats["compressed_size"] / self.stats["total_size"]) * 100
            if self.stats["total_size"] > 0
            else 0
        )

        print(f"\n{ColorText.green('✨ Packing Successful! ✨')}")
        print(f"\n{ColorText.cyan('📊 Packing Statistics:')}")
        print(f"├─ Total files: {ColorText.yellow(str(self.stats['total_files']))}")
        print(
            f"├─ Original size: {ColorText.yellow(self.format_size(self.stats['total_size']))}"
        )
        print(
            f"├─ Final size: {ColorText.yellow(self.format_size(self.stats['compressed_size']))}"
        )
        print(f"├─ Compression ratio: {ColorText.yellow(f'{compression_ratio:.1f}%')}")
        print(f"├─ Processing time: {ColorText.yellow(f'{completion_time:.1f} seconds')}")
        print(f"└─ MTZ file: {ColorText.yellow(absolute_mtz_path)}\n")
        
        self.logger.info(f"Packing completed in {completion_time:.1f} seconds")
        self.logger.info(f"MTZ file created at: {absolute_mtz_path}")