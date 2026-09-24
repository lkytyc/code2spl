import json
import os


class JSONProcessor:
    def process_json(self, file_path, remove_key) -> int:
        data = self.read_json(file_path)
        if data == 0 or data == -1:
            return 0
        if remove_key in data:
            del data[remove_key]
            self.write_json(data, file_path)
            return 1
        return 0

    def read_json(self, file_path: str):
        if not os.path.exists(file_path):
            return 0
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
            return data
        except Exception:
            return -1

    def write_json(self, data, file_path: str) -> int:
        try:
            with open(file_path, "w") as file:
                json.dump(data, file)
            return 1
        except Exception:
            return -1

import os
import stat
import json
import unittest

class JSONProcessorTestReadJson(unittest.TestCase):
    def setUp(self):
        self.processor = JSONProcessor()
        self.test_data = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3"
        }
        self.file_path = "test.json"

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    # file exists
    def test_read_json_1(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.test_data, file)
        result = self.processor.read_json(self.file_path)
        self.assertEqual(result, self.test_data)

    # file not exists
    def test_read_json_2(self):
        result = self.processor.read_json(self.file_path)
        self.assertEqual(result, 0)

    # invalid json file
    def test_read_json_3(self):
        with open(self.file_path, 'w') as file:
            file.write("Invalid JSON")
        result = self.processor.read_json(self.file_path)
        self.assertEqual(result, -1)

    def test_read_json_4(self):
        result = self.processor.read_json('wrong')
        self.assertEqual(result, 0)

    def test_read_json_5(self):
        result = self.processor.read_json('abcd')
        self.assertEqual(result, 0)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
