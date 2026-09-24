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

class PDFHandlerTestMergePdfs(unittest.TestCase):
    def setUp(self) -> None:
        TestPDFHandler.setUpClass()

    def tearDown(self) -> None:
        TestPDFHandler.tearDownClass()

    def test_merge_pdfs(self):
        TestPDFHandler.setUpClass()
        handler = PDFHandler(TestPDFHandler.test_files)
        result = handler.merge_pdfs("merged.pdf")
        self.assertEqual("Merged PDFs saved at merged.pdf", result)
        self.assertTrue(os.path.exists("merged.pdf"))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
