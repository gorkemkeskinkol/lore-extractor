import argparse

class CommandLineInterface:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='LoreExtractor: Parses Markdown files to insert or update lore sections with parallel universe stories.'
        )
        self._setup_arguments()

    def _setup_arguments(self):
        """
        Setup the expected command line arguments
        """
        self.parser.add_argument(
            '--universes', 
            type=int, 
            default=2, 
            help='Number of parallel universe stories to include in each lore section.'
        )
        self.parser.add_argument(
            '--owners', 
            type=int, 
            default=1, 
            help='Number of owners for project. Defines main character count of stories.'
        )
        self.parser.add_argument(
            '--path', 
            type=str, 
            default='.', 
            help='Path to the directory or file to scan for Markdown files.'
        )
        self.parser.add_argument(
            '--output', 
            type=str, 
            help='Path to the output file where the updated Markdown content will be saved.'
        )
        self.parser.add_argument(
            '--recursive',
            action='store_true',
            help='Recursively scan for Markdown files in subdirectories.'
        )
        self.parser.add_argument(
            '--verbose',
            action='store_true',
            help='Increase output verbosity for debugging purposes.'
        )

    def parse_arguments(self):
        """
        Parse the command line arguments and return them.
        """
        args = self.parser.parse_args()
        return args

    def display_help(self):
        """
        Display the help message for the command line tool.
        """
        self.parser.print_help()
