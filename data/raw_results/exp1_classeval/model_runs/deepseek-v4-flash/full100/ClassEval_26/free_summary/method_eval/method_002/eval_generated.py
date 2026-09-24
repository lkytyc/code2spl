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

class CSVProcessorTestProcessCSVData(unittest.TestCase):
    def setUp(self) -> None:
        self.file = 'read_test.csv'
        self.file_process = 'read_test_process.csv'
        with open(self.file, 'w') as f:
            f.write('a,b,c,d\nhElLo,YoU,ME,LoW,aBc')

    def test_process_csv_data_1(self):
        title = ['a', 'b', 'c', 'd']
        data = ['HELLO']
        csvProcessor = CSVProcessor()
        self.assertEqual(1, csvProcessor.process_csv_data(0, self.file))

        read_title, read_data = csvProcessor.read_csv(self.file_process)
        self.assertEqual(read_title, title)
        self.assertEqual(read_data[0], data)

    def test_process_csv_data_2(self):
        title = ['a', 'b', 'c', 'd']
        data = ['YOU']
        csvProcessor = CSVProcessor()
        self.assertEqual(1, csvProcessor.process_csv_data(1, self.file))

        read_title, read_data = csvProcessor.read_csv(self.file_process)
        self.assertEqual(read_title, title)
        self.assertEqual(read_data[0], data)

    def test_process_csv_data_3(self):
        title = ['a', 'b', 'c', 'd']
        data = ['ME']
        csvProcessor = CSVProcessor()
        self.assertEqual(1, csvProcessor.process_csv_data(2, self.file))

        read_title, read_data = csvProcessor.read_csv(self.file_process)
        self.assertEqual(read_title, title)
        self.assertEqual(read_data[0], data)

    def test_process_csv_data_4(self):
        title = ['a', 'b', 'c', 'd']
        data = ['LOW']
        csvProcessor = CSVProcessor()
        self.assertEqual(1, csvProcessor.process_csv_data(3, self.file))

        read_title, read_data = csvProcessor.read_csv(self.file_process)
        self.assertEqual(read_title, title)
        self.assertEqual(read_data[0], data)

    def test_process_csv_data_5(self):
        title = ['a', 'b', 'c', 'd']
        data = ['ABC']
        csvProcessor = CSVProcessor()
        self.assertEqual(1, csvProcessor.process_csv_data(4, self.file))

        read_title, read_data = csvProcessor.read_csv(self.file_process)
        self.assertEqual(read_title, title)
        self.assertEqual(read_data[0], data)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
