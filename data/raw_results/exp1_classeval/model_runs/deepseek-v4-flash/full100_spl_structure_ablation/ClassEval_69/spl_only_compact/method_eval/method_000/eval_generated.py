from PyPDF2 import PdfReader, PdfWriter

class PDFHandler:
    def __init__(self, filepaths):
        self.filepaths = filepaths
        self.readers = [PdfReader(fp) for fp in filepaths]

    def extract_text_from_pdfs(self):
        pdf_texts = []
        for reader in self.readers:
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                pdf_texts.append(page.extract_text())
        return pdf_texts

    def merge_pdfs(self, output_filepath):
        pdf_writer = PdfWriter()
        for reader in self.readers:
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                pdf_writer.add_page(page)
        with open(output_filepath, 'wb') as out:
            pdf_writer.write(out)
        return f"Merged PDFs saved at {output_filepath}"

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
