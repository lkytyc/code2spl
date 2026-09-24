from bs4 import BeautifulSoup
from gensim.utils import decode_htmlentities
import re


class HtmlUtil:
    def __init__(self):
        self.CODE_MARK = '-CODE-'
        self.URL_MARK = '-URL-'
        self.NUMBER_MARK = '-NUMBER-'
        self.PUNCTUATION = {'.', '?', '!', ':', ';', '…', '。', '？', '！', '：', '；'}

    def _ends_with_punctuation(self, text):
        text = text.strip()
        if not text:
            return False
        return text[-1] in self.PUNCTUATION

    def format_line_html_text(self, html_text):
        soup = BeautifulSoup(html_text, 'html.parser')

        # Step 1: Replace <pre> and <blockquote> content with CODE_MARK
        for tag in soup.find_all(['pre', 'blockquote']):
            tag.clear()
            tag.string = self.CODE_MARK

        # Step 2: Reformat <li> items
        for tag in soup.find_all('li'):
            text = tag.get_text().strip()
            if not self._ends_with_punctuation(text):
                text = text + '.'
            tag.string = '[-] ' + text

        # Step 3: Normalize <p> text
        for tag in soup.find_all('p'):
            text = tag.get_text().strip()
            if not text:
                continue
            next_sibling = tag.find_next_sibling()
            if next_sibling and self.CODE_MARK in next_sibling.get_text():
                if not self._ends_with_punctuation(text):
                    tag.string = text + ':'
                else:
                    # Replace trailing punctuation with colon
                    tag.string = text.rstrip(''.join(self.PUNCTUATION)) + ':'
            else:
                if not self._ends_with_punctuation(text):
                    tag.string = text + '.'
                else:
                    tag.string = text

        # Step 4: Extract all text, decode HTML entities, collapse multiple newlines
        raw_text = soup.get_text()
        decoded_text = decode_htmlentities(raw_text)
        normalized_text = re.sub(r'\n{2,}', '\n', decoded_text)
        return normalized_text

    def extract_code_from_html_text(self, html_text):
        formatted_text = self.format_line_html_text(html_text)
        code_count = formatted_text.count(self.CODE_MARK)

        if code_count == 0:
            return []

        soup = BeautifulSoup(html_text, 'html.parser')
        code_blocks = soup.find_all(['pre', 'blockquote'])

        result = []
        for i, tag in enumerate(code_blocks):
            if i >= code_count:
                break
            result.append(tag.get_text())

        return result

import unittest
import sys

class HtmlUtilTestFormatLineFeed(unittest.TestCase):
    def test_format_line_feed_1(self):
        self.assertEqual(HtmlUtil._HtmlUtil__format_line_feed('aaa\n\n\n'), 'aaa\n')

    def test_format_line_feed_2(self):
        self.assertEqual(HtmlUtil._HtmlUtil__format_line_feed('aaa\n\n\n\n'), 'aaa\n')

    def test_format_line_feed_3(self):
        self.assertEqual(HtmlUtil._HtmlUtil__format_line_feed('aaa\n\n\nbbb\n\n'), 'aaa\nbbb\n')

    def test_format_line_feed_4(self):
        self.assertEqual(HtmlUtil._HtmlUtil__format_line_feed('ccc\n\n\n'), 'ccc\n')

    def test_format_line_feed_5(self):
        self.assertEqual(HtmlUtil._HtmlUtil__format_line_feed(''), '')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
