import PyPDF2


class PDFHandler:
    def __init__(self, file_paths):
        self.file_paths = file_paths
        self.readers = [PyPDF2.PdfReader(path) for path in file_paths]

    def merge_pdfs(self, output_filepath):
        writer = PyPDF2.PdfWriter()
        for reader in self.readers:
            for page in reader.pages:
                writer.add_page(page)
        with open(output_filepath, "wb") as output_file:
            writer.write(output_file)
        return f"Merged PDF saved to {output_filepath}"

    def extract_text_from_pdfs(self):
        extracted_text = []
        for reader in self.readers:
            for page in reader.pages:
                extracted_text.append(page.extract_text())
        return extracted_text

import os
import unittest
from PyPDF2 import PdfFileReader
from reportlab.pdfgen import canvas

class TestPDFHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_files = ["test1.pdf", "test2.pdf"]
        cls.test_text = ["This is a test1.", "This is a test2."]
        for i in range(2):
            c = canvas.Canvas(cls.test_files[i])
            c.drawString(100, 100, cls.test_text[i])
            c.showPage()
            c.save()

    @classmethod
    def tearDownClass(cls):
        for filename in cls.test_files:
            os.remove(filename)
        os.remove("merged.pdf")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
