import json
import os

class FileManager:
    @staticmethod
    def save_json(file_path, data):
        """
        Save data to a JSON file.
        :param file_path: Path to the JSON file to be saved.
        :param data: Data to be saved in JSON format.
        """
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    @staticmethod
    def read_json(file_path):
        """
        Read data from a JSON file.
        :param file_path: Path to the JSON file to be read.
        :return: Data read from the JSON file.
        """
        with open(file_path, 'r') as json_file:
            return json.load(json_file)

    @staticmethod
    def read_text(file_path):
        """
        Read text from a file.
        :param file_path: Path to the text file to be read.
        :return: Text read from the file.
        """
        with open(file_path, 'r') as file:
            return file.read()

    @staticmethod
    def save_text(file_path, text):
        """
        Save text to a file.
        :param file_path: Path to the text file to be saved.
        :param text: Text to be saved.
        """
        with open(file_path, 'w') as file:
            file.write(text)

    @staticmethod
    def file_exists(file_path):
        """
        Check if a file exists.
        :param file_path: Path to the file to check.
        :return: True if the file exists, False otherwise.
        """
        return os.path.exists(file_path)

    @staticmethod
    def delete_file(file_path):
        """
        Delete a file.
        :param file_path: Path to the file to be deleted.
        """
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print(f"The file {file_path} does not exist.")

    @staticmethod
    def append_to_text(file_path, text):
        """
        Append text to the end of a file.
        :param file_path: Path to the file.
        :param text: Text to append.
        """
        with open(file_path, 'a') as file:
            file.write(text)
