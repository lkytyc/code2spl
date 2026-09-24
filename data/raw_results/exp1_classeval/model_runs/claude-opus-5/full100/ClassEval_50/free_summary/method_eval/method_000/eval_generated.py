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
