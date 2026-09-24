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

class XMLProcessorTestWriteXml(unittest.TestCase):
    def test_write_xml_1(self):
        with open('test.xml', 'w') as f:
            f.write('<root>\n    <item>apple</item>\n    <item>banana</item>\n    <item>orange</item>\n</root>')
        self.xml_file = 'test.xml'
        self.processor = XMLProcessor(self.xml_file)
        tree = ET.parse(self.processor.file_name)
        self.processor.root = tree.getroot()

        file_name = 'output.xml'
        result = self.processor.write_xml(file_name)
        self.assertTrue(result)

        processor1 = XMLProcessor(file_name)
        tree1 = ET.parse(processor1.file_name)
        processor1.root = tree1.getroot()

        self.assertIsNotNone(processor1.root)
        lst = processor1.root.findall('item')
        self.assertEqual(lst[0].text, 'apple')
        self.assertEqual(lst[1].text, 'banana')
        self.assertEqual(lst[2].text, 'orange')

        os.remove('output.xml')
        os.remove('test.xml')

    def test_write_xml_2(self):
        with open('test.xml', 'w') as f:
            f.write('<root>\n    <item>apple</item>\n    <item>banana</item>\n</root>')
        self.xml_file = 'test.xml'
        self.processor = XMLProcessor(self.xml_file)
        tree = ET.parse(self.processor.file_name)
        self.processor.root = tree.getroot()

        file_name = 'output.xml'
        result = self.processor.write_xml(file_name)
        self.assertTrue(result)

        processor1 = XMLProcessor(file_name)
        tree1 = ET.parse(processor1.file_name)
        processor1.root = tree1.getroot()

        self.assertIsNotNone(processor1.root)
        lst = processor1.root.findall('item')
        self.assertEqual(lst[0].text, 'apple')
        self.assertEqual(lst[1].text, 'banana')

        os.remove('output.xml')
        os.remove('test.xml')

    def test_write_xml_3(self):
        with open('test.xml', 'w') as f:
            f.write('<root>\n    <item>apple</item>\n</root>')
        self.xml_file = 'test.xml'
        self.processor = XMLProcessor(self.xml_file)
        tree = ET.parse(self.processor.file_name)
        self.processor.root = tree.getroot()

        file_name = 'output.xml'
        result = self.processor.write_xml(file_name)
        self.assertTrue(result)

        processor1 = XMLProcessor(file_name)
        tree1 = ET.parse(processor1.file_name)
        processor1.root = tree1.getroot()

        self.assertIsNotNone(processor1.root)
        lst = processor1.root.findall('item')
        self.assertEqual(lst[0].text, 'apple')

        os.remove('output.xml')
        os.remove('test.xml')

    def test_write_xml_4(self):
        with open('test.xml', 'w') as f:
            f.write('<root>\n    <item>aaa</item>\n    <item>bbb</item>\n    <item>ccc</item>\n</root>')
        self.xml_file = 'test.xml'
        self.processor = XMLProcessor(self.xml_file)
        tree = ET.parse(self.processor.file_name)
        self.processor.root = tree.getroot()

        file_name = 'output.xml'
        result = self.processor.write_xml(file_name)
        self.assertTrue(result)

        processor1 = XMLProcessor(file_name)
        tree1 = ET.parse(processor1.file_name)
        processor1.root = tree1.getroot()

        self.assertIsNotNone(processor1.root)
        lst = processor1.root.findall('item')
        self.assertEqual(lst[0].text, 'aaa')
        self.assertEqual(lst[1].text, 'bbb')
        self.assertEqual(lst[2].text, 'ccc')

        os.remove('output.xml')
        os.remove('test.xml')

    def test_write_xml_5(self):
        with open('test.xml', 'w') as f:
            f.write('<root>\n    <item>apple</item>\n    <item>orange</item>\n</root>')
        self.xml_file = 'test.xml'
        self.processor = XMLProcessor(self.xml_file)
        tree = ET.parse(self.processor.file_name)
        self.processor.root = tree.getroot()

        file_name = 'output.xml'
        result = self.processor.write_xml(file_name)
        self.assertTrue(result)

        processor1 = XMLProcessor(file_name)
        tree1 = ET.parse(processor1.file_name)
        processor1.root = tree1.getroot()

        self.assertIsNotNone(processor1.root)
        lst = processor1.root.findall('item')
        self.assertEqual(lst[0].text, 'apple')
        self.assertEqual(lst[1].text, 'orange')

        os.remove('output.xml')
        os.remove('test.xml')

    def test_write_xml_6(self):
        self.xml_file = ''
        self.processor = XMLProcessor(self.xml_file)

        result = self.processor.write_xml("")
        self.assertFalse(result)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
