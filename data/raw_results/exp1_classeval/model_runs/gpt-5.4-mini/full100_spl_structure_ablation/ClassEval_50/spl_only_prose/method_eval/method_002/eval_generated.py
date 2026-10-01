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

class JSONProcessorTestProcessJsonExistingKey(unittest.TestCase):
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

    # key exists
    def test_process_json_1(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.test_data, file)
        remove_key = "key2"
        self.processor.process_json(self.file_path, remove_key)
        with open(self.file_path, 'r') as file:
            processed_data = json.load(file)
        expected_data = {
            "key1": "value1",
            "key3": "value3"
        }
        self.assertEqual(processed_data, expected_data)

    # key not exists
    def test_process_json_2(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.test_data, file)
        remove_key = "nonexistent_key"
        self.processor.process_json(self.file_path, remove_key)
        with open(self.file_path, 'r') as file:
            processed_data = json.load(file)
        self.assertEqual(processed_data, self.test_data)

    # file is empty
    def test_process_json_3(self):
        # Create an empty JSON file
        with open(self.file_path, 'w') as file:
            pass
        remove_key = "key1"
        self.assertEqual(self.processor.process_json(self.file_path, remove_key), 0)

    def test_process_json_4(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.test_data, file)
        remove_key = "aaa"
        self.processor.process_json(self.file_path, remove_key)
        with open(self.file_path, 'r') as file:
            processed_data = json.load(file)
        self.assertEqual(processed_data, self.test_data)

    def test_process_json_5(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.test_data, file)
        remove_key = "bbb"
        self.processor.process_json(self.file_path, remove_key)
        with open(self.file_path, 'r') as file:
            processed_data = json.load(file)
        self.assertEqual(processed_data, self.test_data)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
