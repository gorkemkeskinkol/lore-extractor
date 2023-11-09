import os
from functools import reduce

from Utilities.FileManager import FileManager
from Utilities.LoreManager import LoreManager
from Utilities.DirectoryScanner import DirectoryScanner
from Utilities.CommandLineInterface import CommandLineInterface
from Utilities.MarkdownParser import MarkdownParser

class Lore:
    def __init__(self, args):
        self.args = args
        self.update()

    def update(self):
        # Kullanıcı tarafından sağlanan yolun geçerli bir dizin olup olmadığını kontrol et
        if not os.path.isdir(args.path):
            print(f"Hata: Belirtilen yol geçerli bir dizin değil - {args.path}")
            cli.display_help()
        else:
            # Dizin tarayıcısını başlat ve tarama yap
            scanner = DirectoryScanner(start_path=args.path, file_extension='.md', recursive=args.recursive)
            markdown_files = scanner.scan_directories()

            # Her bir Markdown dosyasını işle
            parser = MarkdownParser(num_parallel_universes=args.universes)
            for directory, files in markdown_files.items():
                for file in files:
                    file_path = os.path.join(directory, file)
                    # Eğer dosya varsa ve Markdown uzantısına sahipse işle
                    if FileManager.file_exists(file_path) and file_path.endswith('.md'):
                        with open(file_path, 'r') as md_file:
                            content = md_file.readlines()
                        updated_content = parser.parse_markdown(content)
                        if args.output:
                            # Güncellenmiş içeriği belirtilen çıkış dosyasına yaz
                            output_path = os.path.join(args.output, file)
                            FileManager.save_text(output_path, ''.join(updated_content))
                        else:
                            # Güncellenmiş içeriği orijinal dosyaya yaz
                            FileManager.save_text(file_path, ''.join(updated_content))
                        print(f"{file_path} başarıyla güncellendi.")

            print("Tüm Markdown dosyaları işlendi.")
            
if __name__ == "__main__":
    # Komut satırı argümanlarını işle
    cli = CommandLineInterface()
    args = cli.parse_arguments()

    # Lore nesnesini başlat ve güncelle
    Lore(args)

