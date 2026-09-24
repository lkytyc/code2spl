class XMLProcessor:
    def __init__(self, file_name):
        self.file_name = file_name
        self.root = None

    def read_file(self):
        try:
            import xml.etree.ElementTree as ET
            tree = ET.parse(self.file_name)
            self.root = tree.getroot()
            return self.root
        except Exception:
            return None

    def modify_items(self):
        if self.root is None:
            return False
        try:
            for elem in self.root.iter('item'):
                if elem.text:
                    elem.text = elem.text.upper()
            return True
        except Exception:
            return False

    def write_file(self, output_file=None):
        if self.root is None:
            return False
        try:
            import xml.etree.ElementTree as ET
            target = output_file if output_file else self.file_name
            tree = ET.ElementTree(self.root)
            tree.write(target, encoding='utf-8', xml_declaration=True)
            return True
        except Exception:
            return False

    def find_elements(self, tag_name):
        if self.root is None:
            return []
        return self.root.findall('.//' + tag_name)

import unittest
import os

class XMLProcessorTestFindElement(unittest.TestCase):
    def test_find_element_1(self):
        with open('test.xml', 'w') as f:
            f.write('<root>\n    <item>apple</item>\n    <item>banana</item>\n    <item>orange</item>\n</root>')
        self.xml_file = 'test.xml'
        self.processor = XMLProcessor(self.xml_file)
        tree = ET.parse(self.processor.file_name)
        self.processor.root = tree.getroot()

        element_name = 'item'
        root = self.processor.read_xml()
        elements = self.processor.find_element(element_name)
        self.assertEqual(len(elements), 3)
        self.assertEqual(elements[0].text, 'apple')
        self.assertEqual(elements[1].text, 'banana')
        self.assertEqual(elements[2].text, 'orange')

        os.remove('test.xml')

    def test_find_element_2(self):
        with open('test.xml', 'w') as f:
            f.write('<root>\n    <item>apple</item>\n    <item>banana</item>\n</root>')
        self.xml_file = 'test.xml'
        self.processor = XMLProcessor(self.xml_file)
        tree = ET.parse(self.processor.file_name)
        self.processor.root = tree.getroot()

        element_name = 'item'
        root = self.processor.read_xml()
        elements = self.processor.find_element(element_name)
        self.assertEqual(len(elements), 2)
        self.assertEqual(elements[0].text, 'apple')
        self.assertEqual(elements[1].text, 'banana')

        os.remove('test.xml')

    def test_find_element_3(self):
        with open('test.xml', 'w') as f:
            f.write('<root>\n    <item>apple</item>\n</root>')
        self.xml_file = 'test.xml'
        self.processor = XMLProcessor(self.xml_file)
        tree = ET.parse(self.processor.file_name)
        self.processor.root = tree.getroot()

        element_name = 'item'
        root = self.processor.read_xml()
        elements = self.processor.find_element(element_name)
        self.assertEqual(len(elements), 1)
        self.assertEqual(elements[0].text, 'apple')

        os.remove('test.xml')

    def test_find_element_4(self):
        with open('test.xml', 'w') as f:
            f.write('<root>\n    <item>apple</item>\n    <item>orange</item>\n</root>')
        self.xml_file = 'test.xml'
        self.processor = XMLProcessor(self.xml_file)
        tree = ET.parse(self.processor.file_name)
        self.processor.root = tree.getroot()

        element_name = 'item'
        root = self.processor.read_xml()
        elements = self.processor.find_element(element_name)
        self.assertEqual(len(elements), 2)
        self.assertEqual(elements[0].text, 'apple')
        self.assertEqual(elements[1].text, 'orange')

        os.remove('test.xml')

    def test_find_element_5(self):
        with open('test.xml', 'w') as f:
            f.write('<root>\n    <item>aaa</item>\n    <item>bbb</item>\n    <item>ccc</item>\n</root>')
        self.xml_file = 'test.xml'
        self.processor = XMLProcessor(self.xml_file)
        tree = ET.parse(self.processor.file_name)
        self.processor.root = tree.getroot()

        element_name = 'item'
        root = self.processor.read_xml()
        elements = self.processor.find_element(element_name)
        self.assertEqual(len(elements), 3)
        self.assertEqual(elements[0].text, 'aaa')
        self.assertEqual(elements[1].text, 'bbb')
        self.assertEqual(elements[2].text, 'ccc')

        os.remove('test.xml')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
