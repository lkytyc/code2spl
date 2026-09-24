import csv


class CSVProcessor:

    def read_csv(self, file_path):
        with open(file_path, 'r', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)
        title = rows[0] if rows else []
        data = rows[1:] if len(rows) > 1 else []
        return title, data

    def write_csv(self, file_path, rows):
        try:
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            return 1
        except:
            return 0

    def process_csv_data(self, file_path, n):
        title, data = self.read_csv(file_path)
        column_values = [row[n].upper() for row in data]
        base = file_path.split('.')[0]
        ext = '.' + file_path.split('.')[1] if '.' in file_path else ''
        output_path = base + '_process' + ext
        self.write_csv(output_path, [title, column_values])

import unittest
import os

class CSVProcessorTestReadCSV(unittest.TestCase):
    def test_read_csv_1(self):
        self.file = 'read_test.csv'

        with open(self.file, 'w') as f:
            f.write('a,b,c,d\nhElLo,YoU,ME,LoW')

        expected_title = ['a', 'b', 'c', 'd']
        expected_data = [['hElLo', 'YoU', 'ME', 'LoW']]
        csvProcessor = CSVProcessor()
        title, data = csvProcessor.read_csv(self.file)
        self.assertEqual(expected_data, data)
        self.assertEqual(expected_title, title)

    def test_read_csv_2(self):
        self.file = 'read_test.csv'
        with open(self.file, 'w') as f:
            f.write('1234\nhElLo,YoU,ME,LoW')

        expected_title = ['1234']
        expected_data = [['hElLo', 'YoU', 'ME', 'LoW']]
        csvProcessor = CSVProcessor()
        title, data = csvProcessor.read_csv(self.file)
        self.assertEqual(expected_data, data)
        self.assertEqual(expected_title, title)

    def test_read_csv_3(self):
        self.file = 'read_test.csv'

        with open(self.file, 'w') as f:
            f.write('title\nhElLo,YoU,ME,LoW')

        expected_title = ['title']
        expected_data = [['hElLo', 'YoU', 'ME', 'LoW']]
        csvProcessor = CSVProcessor()
        title, data = csvProcessor.read_csv(self.file)
        self.assertEqual(expected_data, data)
        self.assertEqual(expected_title, title)

    def test_read_csv_4(self):
        self.file = 'read_test.csv'

        with open(self.file, 'w') as f:
            f.write('title4\nhElLo,YoU,ME,LoW')

        expected_title = ['title4']
        expected_data = [['hElLo', 'YoU', 'ME', 'LoW']]
        csvProcessor = CSVProcessor()
        title, data = csvProcessor.read_csv(self.file)
        self.assertEqual(expected_data, data)
        self.assertEqual(expected_title, title)

    def test_read_csv_5(self):
        self.file = 'read_test.csv'

        with open(self.file, 'w') as f:
            f.write('title5\nhElLo,YoU,ME,LoW')

        expected_title = ['title5']
        expected_data = [['hElLo', 'YoU', 'ME', 'LoW']]
        csvProcessor = CSVProcessor()
        title, data = csvProcessor.read_csv(self.file)
        self.assertEqual(expected_data, data)
        self.assertEqual(expected_title, title)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
