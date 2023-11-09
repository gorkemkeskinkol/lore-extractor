import os

class DirectoryScanner:
    def __init__(self, start_path='.', file_extension='.md', recursive=True):
        self.start_path = start_path
        self.file_extension = file_extension
        self.recursive = recursive

    def scan_directories(self):
        """
        Scan directories starting from the start path for files with the given file extension.
        :return: A dictionary with keys as directory paths and values as lists of files.
        """
        tree = {}
        for root, dirs, files in os.walk(self.start_path):
            if not self.recursive:
                # Do not dive into subdirectories
                dirs[:] = []
            filtered_files = [f for f in files if f.endswith(self.file_extension)]
            if filtered_files:
                tree[root] = filtered_files
        return tree

    def get_directory_structure(self):
        """
        Get a nested dictionary that represents the folder structure of root directory.
        """
        dir_structure = {}
        for dirpath, dirnames, filenames in os.walk(self.start_path):
            if not self.recursive:
                dirnames[:] = []
            path = dirpath.split(os.sep)
            subdir = dict.fromkeys(filenames)
            parent = reduce(dict.get, path[:-1], dir_structure)
            parent[path[-1]] = subdir
        return dir_structure

    def scan_specific_extension(self, extension):
        """
        Change the file extension to scan for.
        """
        self.file_extension = extension
        return self.scan_directories()

    def is_path_valid(self):
        """
        Check if the start path is a valid directory.
        """
        return os.path.isdir(self.start_path)
