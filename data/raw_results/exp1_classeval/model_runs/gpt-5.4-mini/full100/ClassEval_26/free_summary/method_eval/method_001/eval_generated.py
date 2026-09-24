class CSVProcessor:
    def __init__(self):
        pass

    def read_csv(self, file_name):
        import csv
        with open(file_name, "r", newline="") as f:
            reader = csv.reader(f)
            rows = list(reader)
        header = rows[0] if rows else []
        data_rows = rows[1:] if len(rows) > 1 else []
        return header, data_rows

    def write_csv(self, data, file_name):
        import csv
        try:
            with open(file_name, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(data)
            return 1
        except Exception:
            return 0

    def process_csv_data(self, N, save_file_name):
        import os
        header, rows = self.read_csv(save_file_name)
        processed_values = []
        for row in rows:
            if N < len(row):
                processed_values.append(row[N].upper())
            else:
                processed_values.append("")
        result = [header, processed_values]
        base, _ = os.path.splitext(save_file_name)
        new_file_name = base + "_process.csv"
        return self.write_csv(result, new_file_name)

import unittest
import os

class CSVProcessorTestWriteCSV(unittest.TestCase):
    def test_write_csv_1(self):
        self.file = 'read_test.csv'

        file_path = self.file
        csvProcessor = CSVProcessor()
        data = [['a', 'b', 'c', 'd'], ['1', '2', '3', '4']]
        # assert return value
        self.assertEqual(1, csvProcessor.write_csv(data, file_path))

        # read to test if write correctly
        read_title, read_data = csvProcessor.read_csv(file_path)
        self.assertEqual(read_title, data[0])
        self.assertEqual(read_data[0], data[1])
        os.remove(file_path)

    def test_write_csv_2(self):
        self.file = 'read_test.csv'

        file_path = self.file
        csvProcessor = CSVProcessor()
        data = [['aa', 'bb', 'cc', 'dd'], ['1', '2', '3', '4']]
        # assert return value
        self.assertEqual(1, csvProcessor.write_csv(data, file_path))

        # read to test if write correctly
        read_title, read_data = csvProcessor.read_csv(file_path)
        self.assertEqual(read_title, data[0])
        self.assertEqual(read_data[0], data[1])
        os.remove(file_path)

    def test_write_csv_3(self):
        self.file = 'read_test.csv'

        file_path = self.file
        csvProcessor = CSVProcessor()
        data = [['a', 'b', 'c', 'd'], ['11', '22', '33', '44']]
        # assert return value
        self.assertEqual(1, csvProcessor.write_csv(data, file_path))

        # read to test if write correctly
        read_title, read_data = csvProcessor.read_csv(file_path)
        self.assertEqual(read_title, data[0])
        self.assertEqual(read_data[0], data[1])
        os.remove(file_path)

    def test_write_csv_4(self):
        self.file = 'read_test.csv'

        file_path = self.file
        csvProcessor = CSVProcessor()
        data = [['e', 'f', 'g', 'h'], ['1', '2', '3', '4']]
        # assert return value
        self.assertEqual(1, csvProcessor.write_csv(data, file_path))

        # read to test if write correctly
        read_title, read_data = csvProcessor.read_csv(file_path)
        self.assertEqual(read_title, data[0])
        self.assertEqual(read_data[0], data[1])
        os.remove(file_path)

    def test_write_csv_5(self):
        self.file = 'read_test.csv'

        file_path = self.file
        csvProcessor = CSVProcessor()
        data = [['a', 'b', 'c', 'd'], ['5', '6', '7', '8']]
        # assert return value
        self.assertEqual(1, csvProcessor.write_csv(data, file_path))

        # read to test if write correctly
        read_title, read_data = csvProcessor.read_csv(file_path)
        self.assertEqual(read_title, data[0])
        self.assertEqual(read_data[0], data[1])
        os.remove(file_path)

    def test_write_csv_6(self):
        self.file = ''
        file_path = self.file
        csvProcessor = CSVProcessor()
        # assert return value
        self.assertEqual(0, csvProcessor.write_csv([], file_path))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
