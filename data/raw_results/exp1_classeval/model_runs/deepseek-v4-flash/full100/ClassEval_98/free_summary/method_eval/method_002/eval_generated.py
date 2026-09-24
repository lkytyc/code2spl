import xml.etree.ElementTree as ET


class XMLProcessor:
    def __init__(self, filename):
        self.filename = filename
        self.tree = None

    def read_xml(self):
        try:
            self.tree = ET.parse(self.filename)
            return self.tree
        except (ET.ParseError, OSError, ValueError, TypeError):
            self.tree = None
            return None

    def write_xml(self, filename=None):
        if self.tree is None:
            return False
        try:
            output = filename if filename is not None else self.filename
            self.tree.write(output, encoding="utf-8", xml_declaration=False)
            return True
        except (OSError, ValueError, TypeError):
            return False

    def process_xml_data(self):
        if self.tree is None and self.read_xml() is None:
            return False

        root = self.tree.getroot()
        for item in root.iter("item"):
            if item.text:
                item.text = item.text.upper()

        return self.write_xml()

    def find_element(self, name):
        if self.tree is None and self.read_xml() is None:
            return None

        return list(self.tree.getroot().iter(name))

import unittest
import os

class XMLProcessorTestProcessXmlData(unittest.TestCase):
    def test_process_xml_data_1(self):
        with open('test.xml', 'w') as f:
            f.write('<root>\n    <item>apple</item>\n    <item>banana</item>\n    <item>orange</item>\n</root>')
        self.xml_file = 'test.xml'
        self.processor = XMLProcessor(self.xml_file)
        tree = ET.parse(self.processor.file_name)
        self.processor.root = tree.getroot()

        file_name = 'processed.xml'
        result = self.processor.process_xml_data(file_name)
        self.assertTrue(result)

        processor1 = XMLProcessor(file_name)
        tree1 = ET.parse(processor1.file_name)
        processor1.root = tree1.getroot()

        self.assertIsNotNone(processor1.root)
        lst = processor1.root.findall('item')
        self.assertEqual(lst[0].text, 'APPLE')
        self.assertEqual(lst[1].text, 'BANANA')
        self.assertEqual(lst[2].text, 'ORANGE')

        os.remove('processed.xml')
        os.remove('test.xml')

    def test_process_xml_data_2(self):
        with open('test.xml', 'w') as f:
            f.write('<root>\n    <item>apple</item>\n    <item>banana</item>\n</root>')
        self.xml_file = 'test.xml'
        self.processor = XMLProcessor(self.xml_file)
        tree = ET.parse(self.processor.file_name)
        self.processor.root = tree.getroot()

        file_name = 'processed.xml'
        result = self.processor.process_xml_data(file_name)
        self.assertTrue(result)

        processor1 = XMLProcessor(file_name)
        tree1 = ET.parse(processor1.file_name)
        processor1.root = tree1.getroot()

        self.assertIsNotNone(processor1.root)
        lst = processor1.root.findall('item')
        self.assertEqual(lst[0].text, 'APPLE')
        self.assertEqual(lst[1].text, 'BANANA')

        os.remove('processed.xml')
        os.remove('test.xml')

    def test_process_xml_data_3(self):
        with open('test.xml', 'w') as f:
            f.write('<root>\n    <item>apple</item>\n</root>')
        self.xml_file = 'test.xml'
        self.processor = XMLProcessor(self.xml_file)
        tree = ET.parse(self.processor.file_name)
        self.processor.root = tree.getroot()

        file_name = 'processed.xml'
        result = self.processor.process_xml_data(file_name)
        self.assertTrue(result)

        processor1 = XMLProcessor(file_name)
        tree1 = ET.parse(processor1.file_name)
        processor1.root = tree1.getroot()

        self.assertIsNotNone(processor1.root)
        lst = processor1.root.findall('item')
        self.assertEqual(lst[0].text, 'APPLE')

        os.remove('processed.xml')
        os.remove('test.xml')

    def test_process_xml_data_4(self):
        with open('test.xml', 'w') as f:
            f.write('<root>\n    <item>apple</item>\n    <item>orange</item>\n</root>')
        self.xml_file = 'test.xml'
        self.processor = XMLProcessor(self.xml_file)
        tree = ET.parse(self.processor.file_name)
        self.processor.root = tree.getroot()

        file_name = 'processed.xml'
        result = self.processor.process_xml_data(file_name)
        self.assertTrue(result)

        processor1 = XMLProcessor(file_name)
        tree1 = ET.parse(processor1.file_name)
        processor1.root = tree1.getroot()

        self.assertIsNotNone(processor1.root)
        lst = processor1.root.findall('item')
        self.assertEqual(lst[0].text, 'APPLE')
        self.assertEqual(lst[1].text, 'ORANGE')

        os.remove('processed.xml')
        os.remove('test.xml')

    def test_process_xml_data_5(self):
        with open('test.xml', 'w') as f:
            f.write('<root>\n    <item>aaa</item>\n    <item>bbb</item>\n    <item>ccc</item>\n</root>')
        self.xml_file = 'test.xml'
        self.processor = XMLProcessor(self.xml_file)
        tree = ET.parse(self.processor.file_name)
        self.processor.root = tree.getroot()

        file_name = 'processed.xml'
        result = self.processor.process_xml_data(file_name)
        self.assertTrue(result)

        processor1 = XMLProcessor(file_name)
        tree1 = ET.parse(processor1.file_name)
        processor1.root = tree1.getroot()

        self.assertIsNotNone(processor1.root)
        lst = processor1.root.findall('item')
        self.assertEqual(lst[0].text, 'AAA')
        self.assertEqual(lst[1].text, 'BBB')
        self.assertEqual(lst[2].text, 'CCC')

        os.remove('processed.xml')
        os.remove('test.xml')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
