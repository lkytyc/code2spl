import csv

class CSVProcessor:
    def __init__(self):
        pass

    def read_csv(self, file_name):
        data = []
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            title = next(reader)
            for row in reader:
                data.append(row)
        return (title, data)

    def write_csv(self, data, file_name):
        try:
            with open(file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)
            return 1
        except Exception:
            return 0

    def process_csv_data(self, N, save_file_name):
        title, data = self.read_csv(save_file_name)
        column_data = [row[N] for row in data]
        column_data = [item.upper() for item in column_data]
        new_data = [title, column_data]
        output_file_name = save_file_name.split('.')[0] + '_process.csv'
        return self.write_csv(new_data, output_file_name)

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
