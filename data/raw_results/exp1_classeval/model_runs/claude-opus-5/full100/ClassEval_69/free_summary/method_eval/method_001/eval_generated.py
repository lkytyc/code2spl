from pypdf import PdfReader, PdfWriter


class PDFHandler:
    def __init__(self, file_paths: list[str]):
        self.readers = [PdfReader(path) for path in file_paths]

    def merge_pdfs(self, output_filepath: str) -> str:
        writer = PdfWriter()
        for reader in self.readers:
            for page in reader.pages:
                writer.add_page(page)
        with open(output_filepath, "wb") as f:
            writer.write(f)
        return f"Merged PDF written to {output_filepath}"

    def extract_text_from_pdfs(self) -> list[str]:
        texts = []
        for reader in self.readers:
            for page in reader.pages:
                texts.append(page.extract_text())
        return texts

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
