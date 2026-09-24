import os
import json

class JSONProcessor:
    def process_json(self, file_path: str, remove_key: str) -> int:
        data = self.read_json(file_path)
        if data == 0 or data == -1:
            return 0
        if remove_key not in data:
            return 0
        del data[remove_key]
        self.write_json(data, file_path)
        return 1

    def read_json(self, file_path: str):
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    return data
            except Exception:
                return -1
        else:
            return 0

    def write_json(self, data, file_path: str) -> int:
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file)
            return 1
        except Exception:
            return -1

import os
import stat
import json
import unittest

class JSONProcessorTestWriteJson(unittest.TestCase):
    def setUp(self):
        self.processor = JSONProcessor()
        self.test_data = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3"
        }
        self.file_path = "test.json"

        # create a read only file
        self.file_path_only_read = 'test_only_read.json'
        with open(self.file_path_only_read, 'w') as f:
            f.write('{"key1": "value1"}')

        # set file only read mode
        os.chmod(self.file_path_only_read, stat.S_IRUSR + stat.S_IRGRP + stat.S_IROTH)

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        if os.path.exists(self.file_path_only_read):
            # unset file only read mode and remove the file
            os.chmod(self.file_path_only_read,
                     stat.S_IWUSR + stat.S_IRUSR + stat.S_IWGRP + stat.S_IRGRP + stat.S_IWOTH + stat.S_IROTH)
            os.remove(self.file_path_only_read)

    def test_write_json_1(self):
        result = self.processor.write_json(self.test_data, self.file_path)
        self.assertEqual(result, 1)
        with open(self.file_path, 'r') as file:
            written_data = json.load(file)
        self.assertEqual(written_data, self.test_data)

    def test_write_json_2(self):
        # Provide a read-only file path to simulate an exception
        result = self.processor.write_json(self.test_data, self.file_path_only_read)
        self.assertEqual(result, -1)

    def test_write_json_3(self):
        result = self.processor.write_json([], self.file_path_only_read)
        self.assertEqual(result, -1)

    def test_write_json_4(self):
        result = self.processor.write_json(self.test_data, '')
        self.assertEqual(result, -1)

    def test_write_json_5(self):
        result = self.processor.write_json([], '')
        self.assertEqual(result, -1)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
