import re

from Utilities.LoreManager import LoreManager

class MarkdownParser:
    def __init__(self, num_parallel_universes):
        self.num_parallel_universes = num_parallel_universes
        self.LoreManager = LoreManager()

    def tag(self, name):
        return f"<!-- {name} -->"

    def add_lore_to_file(self, file_content):
        lore_tag = self.tag('Lore') + '\n' + self.tag('/Lore')
        if lore_tag not in file_content:
            title_index = next((i for i, line in enumerate(file_content) if line.startswith('#')), None)
            if title_index is not None:
                file_content.insert(title_index + 1, lore_tag)
            else:
                file_content.insert(0, lore_tag)
        return file_content

    def add_parallel_universes(self, file_content):
        lore_block_index = file_content.index(self.tag('Lore')) + 1
        story_data = self.LoreManager.get_new_stories()
        for index, data in enumerate(story_data):
            universe_tag = self.tag(f'Parallel Universe {index}') + '\n' + data.title + '\n' + data.story + '\n' + self.tag(f'/Parallel Universe {index}')
            file_content.insert(lore_block_index, universe_tag)
            lore_block_index += 1
        return file_content

    def update_lore_block(self, file_content):
        file_content = self.add_lore_to_file(file_content)
        current_universe_count = self.get_current_universe_count(file_content)
        if current_universe_count < self.num_parallel_universes:
            file_content = self.add_parallel_universes(file_content)
        elif current_universe_count > self.num_parallel_universes:
            file_content = self.trim_excess_universes(file_content, current_universe_count)
        return file_content

    def trim_excess_universes(self, file_content, current_universe_count):
        for index in range(current_universe_count - 1, self.num_parallel_universes - 1, -1):
            universe_end_tag = self.tag(f'/parallel universe {index}')
            if universe_end_tag in file_content:
                universe_start_index = file_content.index(self.tag(f'parallel universe {index}'))
                universe_end_index = file_content.index(universe_end_tag, universe_start_index)
                del file_content[universe_start_index:universe_end_index + 1]
        return file_content

    def get_current_universe_count(self, file_content):
        return sum(1 for line in file_content if 'parallel universe' in line)

    def parse_markdown(self, file_path):
        """
        Belirtilen dosya yolu üzerindeki Markdown dosyasını işler.
        Eğer lore blokları yoksa ekler, varsa günceller.
        """
        # Dosya içeriğini oku
        with open(file_path, 'r') as file:
            content = file.readlines()

        # Lore bloğunu kontrol et ve güncelle
        content = self.ensure_lore_block(content)
        content = self.ensure_universe_blocks(content)

        # Değişiklikleri dosyaya yaz
        with open(file_path, 'w') as file:
            file.writelines(content)

    def ensure_lore_block(self, content):
        """
        Lore bloğunun varlığını kontrol eder ve yoksa ekler.
        """
        if self.tag('Lore') not in content:
            title_index = next((i for i, line in enumerate(content) if line.startswith('#')), None)
            if title_index is not None:
                content.insert(title_index + 1, self.tag('Lore') + self.tag('/Lore'))
            else:
                content.insert(0, self.tag('Lore') + self.tag('/Lore'))
        return content

    def get_current_universe_count(self, content):
        pattern = re.compile(self.tag('Parallel Universe') + r'\s*(\d+)' + self.tag('/Parallel Universe'))
        return len(pattern.findall('\n'.join(content)))

    def ensure_universe_blocks(self, content):
        """
        Lore bloğu içindeki paralel evren sayısını kontrol eder ve gerekirse günceller.
        """
        # Düzenli ifade ile herhangi bir numarayı içeren etiketleri bul
        lore_block_index = content.index(self.tag('Lore')) + 1
        pattern = re.compile(self.tag('Parallel Universe') + r'\s*(\d+)')
        current_universe_count = len(pattern.findall('\n'.join(content)))
        
        # Eksik paralel evrenleri ekle
        while current_universe_count < self.num_parallel_universes:
            universe_tag = self.tag(f'Parallel Universe {current_universe_count}') + '\n' + self.tag(f'/Parallel Universe {current_universe_count}')
            content.insert(lore_block_index, universe_tag)
            current_universe_count += 1
            lore_block_index += 1  # Eklenen içerikten sonra doğru konuma atlamak için
        
        # Fazla paralel evrenleri sil
        matches = pattern.finditer('\n'.join(content))
        for match in matches:
            if current_universe_count > self.num_parallel_universes:
                start, end = match.span()
                # İçeriği silerken konumları satır bazında ayarlayın
                start_line = start // (len(content[0]) + 1)
                end_line = end // (len(content[0]) + 1)
                del content[start_line:end_line + 1]
                current_universe_count -= 1
            else:
                break
        
        return content
