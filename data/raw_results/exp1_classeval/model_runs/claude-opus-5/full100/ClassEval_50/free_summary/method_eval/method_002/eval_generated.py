import json
import os


class JSONProcessor:
    """Reads, writes, and edits JSON files on disk."""

    def read_json(self, file_path):
        """
        Read and parse a JSON file.

        Returns the parsed Python object on success,
        0 if the file does not exist, -1 on any other error.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return 0
        except Exception:
            return -1

    def write_json(self, data, file_path):
        """
        Serialize data to JSON and write it to file_path.

        Returns 1 on success, -1 on failure.
        """
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return 1
        except Exception:
            return -1

    def process_json(self, file_path, key):
        """
        Remove key from the top-level object in file_path and write it back.

        Returns 1 if the key was found and the file was updated successfully.
        Returns 0 if the file was missing/unreadable or the key was not present.

        Note: this method uses a sentinel object to distinguish a valid read
        result (including the integers 0 and -1) from the error codes that
        read_json returns for missing/failed files.
        """
        _MISSING = object()

        raw = _MISSING
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except FileNotFoundError:
            return 0
        except Exception:
            return 0

        if not isinstance(raw, dict) or key not in raw:
            return 0

        del raw[key]

        result = self.write_json(raw, file_path)
        return 1 if result == 1 else 0

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
