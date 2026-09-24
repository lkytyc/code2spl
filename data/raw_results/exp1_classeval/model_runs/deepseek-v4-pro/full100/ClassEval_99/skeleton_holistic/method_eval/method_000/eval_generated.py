import zipfile


class ZipFileProcessor:
    """
    This is a compressed file processing class that provides the ability to read and decompress compressed files
    """

    def __init__(self, file_name):
        """
        Initialize file name
        :param file_name:string
        """
        self.file_name = file_name

    def read_zip_file(self):
        """
        Get open file object
        :return:If successful, returns the open file object; otherwise, returns None
        >>> zfp = ZipFileProcessor("aaa.zip")
        >>> file = zfp.read_zip_file()
        """
        try:
            return zipfile.ZipFile(self.file_name, 'r')
        except (FileNotFoundError, zipfile.BadZipFile):
            return None

    def extract_all(self, output_path):
        """
        Extract all zip files and place them in the specified path
        :param output_path: string, The location of the extracted file
        :return: True or False, representing whether the extraction operation was successful
        >>> zfp = ZipFileProcessor("aaa.zip")
        >>> zfp.extract_all("result/aaa")
        """
        try:
            with zipfile.ZipFile(self.file_name, 'r') as zip_ref:
                zip_ref.extractall(output_path)
            return True
        except (FileNotFoundError, zipfile.BadZipFile, OSError):
            return False

    def extract_file(self, file_name, output_path):
        """
        Extract the file with the specified name from the zip file and place it in the specified path
        :param file_name:string, The name of the file to be uncompressed
        :param output_path:string, The location of the extracted file
        :return: True or False, representing whether the extraction operation was successful
        >>> zfp = ZipFileProcessor("aaa.zip")
        >>> zfp.extract_file("bbb.txt", "result/aaa")
        """
        try:
            with zipfile.ZipFile(self.file_name, 'r') as zip_ref:
                zip_ref.extract(file_name, output_path)
            return True
        except (FileNotFoundError, zipfile.BadZipFile, KeyError, OSError):
            return False

    def create_zip_file(self, files, output_file_name):
        """
        Compress the specified file list into a zip file and place it in the specified path
        :param files:list of string, List of files to compress
        :param output_file_name: string, Specified output path
        :return:True or False, representing whether the compression operation was successful
        >>> zfp = ZipFileProcessor("aaa.zip")
        >>> zfp.create_zip_file(["bbb.txt", "ccc,txt", "ddd.txt"], "output/bcd")
        """
        try:
            with zipfile.ZipFile(output_file_name, 'w') as zip_ref:
                for file in files:
                    zip_ref.write(file)
            return True
        except (FileNotFoundError, OSError):
            return False

import unittest
import os

class ZipFileProcessorTestReadZipFile(unittest.TestCase):
    def test_read_zip_file_1(self):
        test_folder = 'test_folder'
        os.makedirs(test_folder, exist_ok=True)
        example_file_path = os.path.join(test_folder, 'example.txt')
        with open(example_file_path, 'w') as file:
            file.write('This is an example file.')

        zip_file_name = 'example1.zip'
        with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
            zip_file.write(example_file_path, os.path.basename(example_file_path))

        processor = ZipFileProcessor(zip_file_name)

        zip_file = processor.read_zip_file()
        self.assertEqual(zip_file.filename, 'example1.zip')
        self.assertEqual(zip_file.mode, 'r')
        zip_file.close()

        os.remove(zip_file_name)
        os.remove(example_file_path)
        os.rmdir(test_folder)

    def test_read_zip_file_2(self):
        test_folder = 'test_folder'
        os.makedirs(test_folder, exist_ok=True)
        example_file_path = os.path.join(test_folder, 'example.txt')
        with open(example_file_path, 'w') as file:
            file.write('This is an example file.')

        zip_file_name = 'example2.zip'
        with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
            zip_file.write(example_file_path, os.path.basename(example_file_path))

        processor = ZipFileProcessor(zip_file_name)

        zip_file = processor.read_zip_file()
        self.assertEqual(zip_file.filename, 'example2.zip')
        self.assertEqual(zip_file.mode, 'r')
        zip_file.close()

        os.remove(zip_file_name)
        os.remove(example_file_path)
        os.rmdir(test_folder)

    def test_read_zip_file_3(self):
        test_folder = 'test_folder'
        os.makedirs(test_folder, exist_ok=True)
        example_file_path = os.path.join(test_folder, 'example.txt')
        with open(example_file_path, 'w') as file:
            file.write('This is an example file.')

        zip_file_name = 'example3.zip'
        with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
            zip_file.write(example_file_path, os.path.basename(example_file_path))

        processor = ZipFileProcessor(zip_file_name)

        zip_file = processor.read_zip_file()
        self.assertEqual(zip_file.filename, 'example3.zip')
        self.assertEqual(zip_file.mode, 'r')
        zip_file.close()

        os.remove(zip_file_name)
        os.remove(example_file_path)
        os.rmdir(test_folder)

    def test_read_zip_file_4(self):
        test_folder = 'test_folder'
        os.makedirs(test_folder, exist_ok=True)
        example_file_path = os.path.join(test_folder, 'example.txt')
        with open(example_file_path, 'w') as file:
            file.write('This is an example file.')

        zip_file_name = 'example4.zip'
        with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
            zip_file.write(example_file_path, os.path.basename(example_file_path))

        processor = ZipFileProcessor(zip_file_name)

        zip_file = processor.read_zip_file()
        self.assertEqual(zip_file.filename, 'example4.zip')
        self.assertEqual(zip_file.mode, 'r')
        zip_file.close()

        os.remove(zip_file_name)
        os.remove(example_file_path)
        os.rmdir(test_folder)

    def test_read_zip_file_5(self):
        test_folder = 'test_folder'
        os.makedirs(test_folder, exist_ok=True)
        example_file_path = os.path.join(test_folder, 'example.txt')
        with open(example_file_path, 'w') as file:
            file.write('This is an example file.')

        zip_file_name = 'example5.zip'
        with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
            zip_file.write(example_file_path, os.path.basename(example_file_path))

        processor = ZipFileProcessor(zip_file_name)
        output_directory = 'output_directory'
        new_zip_file = 'new_zip_file.zip'

        zip_file = processor.read_zip_file()
        self.assertEqual(zip_file.filename, 'example5.zip')
        self.assertEqual(zip_file.mode, 'r')
        zip_file.close()

        os.remove(zip_file_name)
        os.remove(example_file_path)
        os.rmdir(test_folder)

    def test_read_zip_file_6(self):
        processor = ZipFileProcessor("")

        zip_file = processor.read_zip_file()
        self.assertIsNone(zip_file)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
