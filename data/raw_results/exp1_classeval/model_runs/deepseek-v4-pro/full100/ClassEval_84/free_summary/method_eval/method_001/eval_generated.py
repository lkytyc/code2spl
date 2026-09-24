class TextFileProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_text(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def read_json(self):
        import json
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def write_text(self, content):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def process_file(self):
        content = self.read_text()
        filtered = ''.join(ch for ch in content if ch.isalpha())
        self.write_text(filtered)
        return filtered

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
