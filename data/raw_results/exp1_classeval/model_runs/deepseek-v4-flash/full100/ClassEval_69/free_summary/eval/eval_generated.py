from PyPDF2 import PdfReader, PdfWriter

class PDFHandler:
    def __init__(self, pdf_paths):
        self.pdf_paths = pdf_paths
        self.readers = [PdfReader(path) for path in pdf_paths]

    def merge_pdfs(self, output_path):
        writer = PdfWriter()
        for reader in self.readers:
            for page in reader.pages:
                writer.add_page(page)
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        return f"Merged {len(self.readers)} PDFs into {output_path}"

    def extract_text_from_pdfs(self):
        texts = []
        for reader in self.readers:
            for page in reader.pages:
                texts.append(page.extract_text())
        return texts

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



class PDFHandlerTestExtractTextFromPdfs(unittest.TestCase):
    def setUp(self) -> None:
        TestPDFHandler.setUpClass()

    def test_extract_text_from_pdfs(self):
        TestPDFHandler.setUpClass()
        handler = PDFHandler(TestPDFHandler.test_files)
        result = handler.extract_text_from_pdfs()
        self.assertEqual(result, ["This is a test1.\n", "This is a test2.\n"])


class PDFHandlerTestMain(unittest.TestCase):
    def setUp(self) -> None:
        TestPDFHandler.setUpClass()

    def tearDown(self) -> None:
        TestPDFHandler.tearDownClass()

    def test_main(self):
        TestPDFHandler.setUpClass()
        handler = PDFHandler(TestPDFHandler.test_files)
        result = handler.merge_pdfs("merged.pdf")
        self.assertEqual("Merged PDFs saved at merged.pdf", result)
        self.assertTrue(os.path.exists("merged.pdf"))

        result = handler.extract_text_from_pdfs()
        self.assertEqual(result, ["This is a test1.\n", "This is a test2.\n"])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
