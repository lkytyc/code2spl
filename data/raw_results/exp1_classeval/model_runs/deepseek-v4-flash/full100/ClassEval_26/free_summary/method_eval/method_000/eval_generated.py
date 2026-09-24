import csv

class CSVProcessor:
    def read_csv(self, filename):
        with open(filename, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        if not rows:
            return [], []
        return rows[0], rows[1:]

    def write_csv(self, filename, rows):
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            return 1
        except Exception:
            return 0

    def process(self, column_index, input_filename):
        header, rows = self.read_csv(input_filename)
        if column_index < 0 or column_index >= len(header):
            return 0

        output_filename = self._output_filename(input_filename)
        output_rows = [[header[column_index]]]
        output_rows.extend([row[column_index].upper()] for row in rows)
        return self.write_csv(output_filename, output_rows)

    def _output_filename(self, input_filename):
        if input_filename.lower().endswith('.csv'):
            return input_filename[:-4] + '_process.csv'
        return input_filename + '_process.csv'

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
