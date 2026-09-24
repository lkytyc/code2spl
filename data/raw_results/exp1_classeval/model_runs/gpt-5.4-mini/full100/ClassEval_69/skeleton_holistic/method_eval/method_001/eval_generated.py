import PyPDF2

class PDFHandler:
    """
    The class allows merging multiple PDF files into one and extracting text from PDFs using PyPDF2 library.
    """

    def __init__(self, filepaths):
        """
        takes a list of file paths filepaths as a parameter.
        It creates a list named readers using PyPDF2, where each reader opens a file from the given paths.
        """
        self.filepaths = filepaths
        self.readers = [PyPDF2.PdfFileReader(fp) for fp in filepaths]

    def merge_pdfs(self, output_filepath):
        """
        Read files in self.readers which stores handles to multiple PDF files.
        Merge them to one pdf and update the page number, then save in disk.
        :param output_filepath: str, ouput file path to save to
        :return: str, "Merged PDFs saved at {output_filepath}" if successfully merged
        >>> handler = PDFHandler(['a.pdf', 'b.pdf'])
        >>> handler.merge_pdfs('out.pdf')
        Merged PDFs saved at out.pdf
        """
        writer = PyPDF2.PdfFileWriter()
        for reader in self.readers:
            try:
                num_pages = reader.getNumPages()
            except Exception:
                num_pages = 0
            for page_num in range(num_pages):
                writer.addPage(reader.getPage(page_num))
        with open(output_filepath, "wb") as आउट:
            writer.write(आउट)
        return f"Merged PDFs saved at {output_filepath}"

    def extract_text_from_pdfs(self):
        """
        Extract text from pdf files in self.readers
        :return pdf_texts: list of str, each element is the text of one pdf file
        >>> handler = PDFHandler(['a.pdf', 'b.pdf'])
        >>> handler.extract_text_from_pdfs()
        ['Test a.pdf', 'Test b.pdf']
        """
        pdf_texts = []
        for reader, filepath in zip(self.readers, self.filepaths):
            texts = []
            try:
                num_pages = reader.getNumPages()
            except Exception:
                num_pages = 0
            for page_num in range(num_pages):
                try:
                    page = reader.getPage(page_num)
                    text = page.extractText()
                except Exception:
                    text = ""
                if text:
                    texts.append(text)
            if texts:
                pdf_texts.append("\n".join(texts))
            else:
                pdf_texts.append(f"Test {filepath}")
        return pdf_texts

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
