"""
Menu module for MTZ Tool
Handles main menu display and user interaction
"""

import sys
from src.core.extractor import MTZExtractor
from src.core.compressor import MTZCompressor
from src.utils.colors import ColorText
from src.utils.terminal import clear_screen


class MainMenu:
    """Main menu class for MTZ Tool"""

    def __init__(self):
        self.extractor = MTZExtractor()
        self.compressor = MTZCompressor()

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

    def print_menu(self):
        """Display menu options"""
        print(f"\n{ColorText.cyan('Menu Options:')}")
        print(f"  {ColorText.green('1.')} Extract MTZ File")
        print(f"  {ColorText.green('2.')} Pack to MTZ File")
        print(f"  {ColorText.red('3.')} Exit")
        print()

    def get_choice(self) -> str:
        """Get user menu choice"""
        return input(f"{ColorText.cyan('➤ ')} Choose option (1-3): ").strip()

    def handle_extract(self):
        """Handle MTZ extraction"""
        clear_screen()
        self.extractor.print_banner()
        
        file_path = input(
            f"{ColorText.cyan('📂')} Enter MTZ file location: "
        ).strip()

        if not self.extractor.validate_mtz_file(file_path):
            input(f"\n{ColorText.yellow('Press Enter to continue...')}")
            return

        extract_folder = self.extractor.create_extract_folder(file_path)
        if not extract_folder:
            input(f"\n{ColorText.yellow('Press Enter to continue...')}")
            return

        print(f"\n{ColorText.cyan('⏳')} Starting extraction process...\n")

        if not self.extractor.extract_mtz(file_path, extract_folder):
            input(f"\n{ColorText.yellow('Press Enter to continue...')}")
            return

        self.extractor.process_files(extract_folder)
        self.extractor.show_completion(extract_folder)
        
        input(f"\n{ColorText.yellow('Press Enter to continue...')}")

    def handle_pack(self):
        """Handle MTZ packing"""
        clear_screen()
        self.compressor.print_banner()
        
        main_folder = input(
            f"{ColorText.cyan('📂')} Enter folder location to pack: "
        ).strip()

        if not self.compressor.validate_folder(main_folder):
            input(f"\n{ColorText.yellow('Press Enter to continue...')}")
            return

        print(f"\n{ColorText.cyan('⏳')} Starting packing process...\n")
        
        if self.compressor.pack_to_mtz(main_folder):
            self.compressor.show_completion(main_folder)
        else:
            print(f"\n{ColorText.red('❌ Failed to create MTZ file!')}\n")
        
        input(f"\n{ColorText.yellow('Press Enter to continue...')}")

    def run(self):
        """Run the main menu loop"""
        while True:
            clear_screen()
            self.print_banner()
            self.print_menu()
            
            choice = self.get_choice()

            if choice == "1":
                self.handle_extract()
            elif choice == "2":
                self.handle_pack()
            elif choice == "3":
                clear_screen()
                print(f"\n{ColorText.green('👋 Thank you for using MTZ Tool!')}\n")
                sys.exit(0)
            else:
                print(f"\n{ColorText.red('❌ Invalid option! Please choose 1-3.')}")
                input(f"\n{ColorText.yellow('Press Enter to continue...')}")