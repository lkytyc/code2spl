class PDFHandler:
    def __init__(self, pdf_file_paths):
        from PyPDF2 import PdfReader
        self.readers = [PdfReader(path) for path in pdf_file_paths]

    def merge_pdfs(self, output_file_path):
        from PyPDF2 import PdfWriter
        writer = PdfWriter()
        for reader in self.readers:
            for page in reader.pages:
                writer.add_page(page)
        with open(output_file_path, "wb") as output_file:
            writer.write(output_file)
        return f"Merged PDF saved to {output_file_path}"

    def extract_text_from_pdfs(self):
        page_texts = []
        for reader in self.readers:
            for page in reader.pages:
                page_texts.append(page.extract_text())
        return page_texts

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
