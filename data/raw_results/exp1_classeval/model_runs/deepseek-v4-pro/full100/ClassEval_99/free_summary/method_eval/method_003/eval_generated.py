import zipfile
import os

class ZipFileProcessor:
    def __init__(self, zip_file_name):
        self.zip_file_name = zip_file_name

    def read_zip_file(self):
        try:
            return zipfile.ZipFile(self.zip_file_name, 'r')
        except (FileNotFoundError, zipfile.BadZipFile, OSError):
            return None

    def extract_all(self, output_directory):
        try:
            with zipfile.ZipFile(self.zip_file_name, 'r') as zip_ref:
                zip_ref.extractall(output_directory)
            return True
        except (FileNotFoundError, zipfile.BadZipFile, OSError):
            return False

    def extract_file(self, file_name, output_directory):
        try:
            with zipfile.ZipFile(self.zip_file_name, 'r') as zip_ref:
                zip_ref.extract(file_name, output_directory)
            return True
        except (FileNotFoundError, zipfile.BadZipFile, KeyError, OSError):
            return False

    def create_zip_file(self, file_paths, output_zip_file):
        try:
            with zipfile.ZipFile(output_zip_file, 'w') as zip_ref:
                for file_path in file_paths:
                    zip_ref.write(file_path, os.path.basename(file_path))
            return True
        except (FileNotFoundError, OSError):
            return False

import unittest
import os

class ZipFileProcessorTestCreateZipFile(unittest.TestCase):
    def test_create_zip_file_1(self):
        test_folder = 'test_folder'
        os.makedirs(test_folder, exist_ok=True)
        example_file_path = os.path.join(test_folder, 'example1.txt')
        with open(example_file_path, 'w') as file:
            file.write('This is an example file.')

        zip_file_name = 'example.zip'
        with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
            zip_file.write(example_file_path, os.path.basename(example_file_path))

        processor = ZipFileProcessor(zip_file_name)
        output_directory = 'output_directory'
        new_zip_file = 'new_zip_file.zip'

        files_to_zip = [example_file_path]
        success = processor.create_zip_file(files_to_zip, new_zip_file)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(new_zip_file))

        os.remove(example_file_path)
        os.rmdir(test_folder)

    def test_create_zip_file_2(self):
        test_folder = 'test_folder'
        os.makedirs(test_folder, exist_ok=True)
        example_file_path = os.path.join(test_folder, 'example2.txt')
        with open(example_file_path, 'w') as file:
            file.write('This is an example file.')

        zip_file_name = 'example.zip'
        with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
            zip_file.write(example_file_path, os.path.basename(example_file_path))

        processor = ZipFileProcessor(zip_file_name)
        output_directory = 'output_directory'
        new_zip_file = 'new_zip_file.zip'

        files_to_zip = [example_file_path]
        success = processor.create_zip_file(files_to_zip, new_zip_file)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(new_zip_file))

        os.remove(example_file_path)
        os.rmdir(test_folder)

    def test_create_zip_file_3(self):
        test_folder = 'test_folder'
        os.makedirs(test_folder, exist_ok=True)
        example_file_path = os.path.join(test_folder, 'example3.txt')
        with open(example_file_path, 'w') as file:
            file.write('This is an example file.')

        zip_file_name = 'example.zip'
        with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
            zip_file.write(example_file_path, os.path.basename(example_file_path))

        processor = ZipFileProcessor(zip_file_name)
        output_directory = 'output_directory'
        new_zip_file = 'new_zip_file.zip'

        files_to_zip = [example_file_path]
        success = processor.create_zip_file(files_to_zip, new_zip_file)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(new_zip_file))

        os.remove(example_file_path)
        os.rmdir(test_folder)

    def test_create_zip_file_4(self):
        test_folder = 'test_folder'
        os.makedirs(test_folder, exist_ok=True)
        example_file_path = os.path.join(test_folder, 'example4.txt')
        with open(example_file_path, 'w') as file:
            file.write('This is an example file.')

        zip_file_name = 'example.zip'
        with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
            zip_file.write(example_file_path, os.path.basename(example_file_path))

        processor = ZipFileProcessor(zip_file_name)
        output_directory = 'output_directory'
        new_zip_file = 'new_zip_file.zip'

        files_to_zip = [example_file_path]
        success = processor.create_zip_file(files_to_zip, new_zip_file)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(new_zip_file))

        os.remove(example_file_path)
        os.rmdir(test_folder)

    def test_create_zip_file_5(self):
        test_folder = 'test_folder'
        os.makedirs(test_folder, exist_ok=True)
        example_file_path = os.path.join(test_folder, 'example5.txt')
        with open(example_file_path, 'w') as file:
            file.write('This is an example file.')

        zip_file_name = 'example.zip'
        with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
            zip_file.write(example_file_path, os.path.basename(example_file_path))

        processor = ZipFileProcessor(zip_file_name)
        new_zip_file = 'new_zip_file.zip'

        files_to_zip = [example_file_path]
        success = processor.create_zip_file(files_to_zip, new_zip_file)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(new_zip_file))

        os.remove(example_file_path)
        os.rmdir(test_folder)

    def test_create_zip_file_6(self):
        processor = ZipFileProcessor("")

        success = processor.create_zip_file("", "")
        self.assertFalse(success)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
