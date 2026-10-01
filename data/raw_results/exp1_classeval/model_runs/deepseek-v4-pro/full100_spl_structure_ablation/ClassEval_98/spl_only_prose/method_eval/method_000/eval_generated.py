import xml.etree.ElementTree as ET


class XMLProcessor:
    def __init__(self, file_name):
        self.file_name = file_name
        self.root = None

    def find_element(self, element_name):
        elements = self.root.findall(element_name)
        return elements

    def process_xml_data(self, file_name):
        for element in self.root.iter('item'):
            text = element.text
            element.text = text.upper()
        return self.write_xml(file_name)

    def read_xml(self):
        try:
            tree = ET.parse(self.file_name)
            self.root = tree.getroot()
            return self.root
        except Exception:
            return None

    def write_xml(self, file_name):
        try:
            tree = ET.ElementTree(self.root)
            tree.write(file_name)
            return True
        except Exception:
            return False

import unittest
import os

class XMLProcessorTestReadXml(unittest.TestCase):
    def test_read_xml_1(self):
        with open('test.xml', 'w') as f:
            f.write('<root>\n    <item>apple</item>\n    <item>banana</item>\n    <item>orange</item>\n</root>')
        self.xml_file = 'test.xml'
        self.processor = XMLProcessor(self.xml_file)
        tree = ET.parse(self.processor.file_name)
        self.processor.root = tree.getroot()

        root = self.processor.read_xml()
        self.assertIsNotNone(root)
        lst = root.findall('item')
        self.assertEqual(lst[0].text, 'apple')
        self.assertEqual(lst[1].text, 'banana')
        self.assertEqual(lst[2].text, 'orange')

        os.remove('test.xml')

    def test_read_xml_2(self):
        with open('test.xml', 'w') as f:
            f.write('<root>\n    <item>aaa</item>\n    <item>bbb</item>\n    <item>ccc</item>\n</root>')
        self.xml_file = 'test.xml'
        self.processor = XMLProcessor(self.xml_file)
        tree = ET.parse(self.processor.file_name)
        self.processor.root = tree.getroot()

        root = self.processor.read_xml()
        self.assertIsNotNone(root)
        lst = root.findall('item')
        self.assertEqual(lst[0].text, 'aaa')
        self.assertEqual(lst[1].text, 'bbb')
        self.assertEqual(lst[2].text, 'ccc')

        os.remove('test.xml')

    def test_read_xml_3(self):
        with open('test.xml', 'w') as f:
            f.write('<root>\n    <item>apple</item>\n</root>')
        self.xml_file = 'test.xml'
        self.processor = XMLProcessor(self.xml_file)
        tree = ET.parse(self.processor.file_name)
        self.processor.root = tree.getroot()

        root = self.processor.read_xml()
        self.assertIsNotNone(root)
        lst = root.findall('item')
        self.assertEqual(lst[0].text, 'apple')

        os.remove('test.xml')

    def test_read_xml_4(self):
        with open('test.xml', 'w') as f:
            f.write('<root>\n    <item>apple</item>\n    <item>banana</item>\n</root>')
        self.xml_file = 'test.xml'
        self.processor = XMLProcessor(self.xml_file)
        tree = ET.parse(self.processor.file_name)
        self.processor.root = tree.getroot()

        root = self.processor.read_xml()
        self.assertIsNotNone(root)
        lst = root.findall('item')
        self.assertEqual(lst[0].text, 'apple')
        self.assertEqual(lst[1].text, 'banana')

        os.remove('test.xml')

    def test_read_xml_5(self):
        with open('test.xml', 'w') as f:
            f.write('<root>\n    <item>apple</item>\n    <item>orange</item>\n</root>')
        self.xml_file = 'test.xml'
        self.processor = XMLProcessor(self.xml_file)
        tree = ET.parse(self.processor.file_name)
        self.processor.root = tree.getroot()

        root = self.processor.read_xml()
        self.assertIsNotNone(root)
        lst = root.findall('item')
        self.assertEqual(lst[0].text, 'apple')
        self.assertEqual(lst[1].text, 'orange')

        os.remove('test.xml')

    def test_read_xml_6(self):
        self.xml_file = ''
        self.processor = XMLProcessor(self.xml_file)

        root = self.processor.read_xml()
        self.assertIsNone(root)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
