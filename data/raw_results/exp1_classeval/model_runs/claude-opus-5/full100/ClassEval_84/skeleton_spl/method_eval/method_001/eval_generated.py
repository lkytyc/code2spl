import json

class TextFileProcessor:
    """
    The class handles reading, writing, and processing text files. It can read the file as JSON, read the raw text, write content to the file, and process the file by removing non-alphabetic characters.
    """

    def __init__(self, file_path):
        """
        Initialize the file path.
        :param file_path: str
        """
        self.file_path = file_path

    def read_file_as_json(self):
        """
        Read the self.file_path file as json format.
        if the file content doesn't obey json format, the code will raise error.
        :return data: dict if the file is stored as json format, or str/int/float.. according to the file content otherwise.
        >>> textFileProcessor = TextFileProcessor('test.json')
        >>> textFileProcessor.read_file_as_json()
        {'name': 'test', 'age': 12}
        >>> type(textFileProcessor.read_file_as_json())
        <class 'dict'>
        """
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        return data

    def read_file(self):
        """
        Read the return the content of self.file_path file.
        :return: the same return as the read() method
        >>> textFileProcessor = TextFileProcessor('test.json')
        >>> textFileProcessor.read_file()
        '{\n    "name": "test",\n    "age": 12\n}'
        """
        with open(self.file_path, 'r') as file_handle:
            return file_handle.read()

    def write_file(self, content):
        """
        Write content into the self.file_path file, and overwrite if the file has already existed.
        :param content: any content
        >>> textFileProcessor = TextFileProcessor('test.json')
        >>> textFileProcessor.write_file('Hello world!')
        >>> textFileProcessor.read_file()
        'Hello world!'
        """
        with open(self.file_path, 'w') as file_handle:
            file_handle.write(content)

    def process_file(self):
        """
        Read the self.file_path file and filter out non-alphabetic characters from the content string.
        Overwrite the after-processed data into the same self.file_path file.
        >>> textFileProcessor = TextFileProcessor('test.json')
        >>> textFileProcessor.read_file()
        '{\n    "name": "test",\n    "age": 12\n}'
        >>> textFileProcessor.process_file()
        'nametestage'
        """
        content = self.read_file()
        content = ''.join(c for c in content if c.isalpha())
        self.write_file(content)
        return content

import unittest
import json
from unittest.mock import MagicMock
import os

class TextFileProcessorTestReadFile(unittest.TestCase):
    def setUp(self) -> None:
        self.files = ['test_1.txt', 'test_2.txt', 'test_3.txt', 'test_4.txt', 'test_5.txt']
        self.contents = ['123aac\n&^(*&43)', '12345', 'aaa', 'bbb', 'ccc']
        for index, file in enumerate(self.files):
            with open(file, 'w') as f:
                f.write(self.contents[index])

    def test_read_file_1(self):
        textFileProcessor = TextFileProcessor(self.files[0])
        data = textFileProcessor.read_file()
        self.assertEqual(str, type(data))
        self.assertEqual(data, self.contents[0])

    def test_read_file_2(self):
        textFileProcessor = TextFileProcessor(self.files[1])
        data = textFileProcessor.read_file()
        self.assertEqual(str, type(data))
        self.assertEqual(data, self.contents[1])

    def test_read_file_3(self):
        textFileProcessor = TextFileProcessor(self.files[2])
        data = textFileProcessor.read_file()
        self.assertEqual(str, type(data))
        self.assertEqual(data, self.contents[2])

    def test_read_file_4(self):
        textFileProcessor = TextFileProcessor(self.files[3])
        data = textFileProcessor.read_file()
        self.assertEqual(str, type(data))
        self.assertEqual(data, self.contents[3])

    def test_read_file_5(self):
        textFileProcessor = TextFileProcessor(self.files[4])
        data = textFileProcessor.read_file()
        self.assertEqual(str, type(data))
        self.assertEqual(data, self.contents[4])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
