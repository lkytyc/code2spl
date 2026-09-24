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
            zip_file = zipfile.ZipFile(self.file_name, "r")
            return zip_file
        except Exception:
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
            with zipfile.ZipFile(self.file_name, "r") as zip_file:
                zip_file.extractall(output_path)
            return True
        except Exception:
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
            with zipfile.ZipFile(self.file_name, "r") as zip_file:
                zip_file.extract(file_name, output_path)
            return True
        except Exception:
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
            with zipfile.ZipFile(output_file_name, "w") as zip_file:
                for current_file in files:
                    zip_file.write(current_file)
            return True
        except Exception:
            return False

import unittest
import os

class ZipFileProcessorTestExtractAll(unittest.TestCase):
    def test_extract_all_1(self):
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

        success = processor.extract_all(output_directory)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(os.path.join(output_directory, 'example1.txt')))

        os.remove(zip_file_name)
        os.remove(example_file_path)
        os.rmdir(test_folder)

    def test_extract_all_2(self):
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

        success = processor.extract_all(output_directory)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(os.path.join(output_directory, 'example2.txt')))

        os.remove(zip_file_name)
        os.remove(example_file_path)
        os.rmdir(test_folder)

    def test_extract_all_3(self):
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

        success = processor.extract_all(output_directory)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(os.path.join(output_directory, 'example3.txt')))

        os.remove(zip_file_name)
        os.remove(example_file_path)
        os.rmdir(test_folder)

    def test_extract_all_4(self):
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

        success = processor.extract_all(output_directory)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(os.path.join(output_directory, 'example4.txt')))

        os.remove(zip_file_name)
        os.remove(example_file_path)
        os.rmdir(test_folder)

    def test_extract_all_5(self):
        test_folder = 'test_folder'
        os.makedirs(test_folder, exist_ok=True)
        example_file_path = os.path.join(test_folder, 'example5.txt')
        with open(example_file_path, 'w') as file:
            file.write('This is an example file.')

        zip_file_name = 'example.zip'
        with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
            zip_file.write(example_file_path, os.path.basename(example_file_path))

        processor = ZipFileProcessor(zip_file_name)
        output_directory = 'output_directory'
        new_zip_file = 'new_zip_file.zip'

        success = processor.extract_all(output_directory)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(os.path.join(output_directory, 'example5.txt')))

        os.remove(zip_file_name)
        os.remove(example_file_path)
        os.rmdir(test_folder)

    def test_extract_all_6(self):
        processor = ZipFileProcessor("")

        success = processor.extract_all("")
        self.assertFalse(success)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
