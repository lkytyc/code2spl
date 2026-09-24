from bs4 import BeautifulSoup
import string
from gensim.utils import decode_htmlentities


class HtmlUtil:
    def __init__(self):
        self.SPACE_MARK = '-SPACE-'
        self.JSON_MARK = '-JSON-'
        self.MARKUP_LANGUAGE_MARK = '-MARKUP_LANGUAGE-'
        self.URL_MARK = '-URL-'
        self.NUMBER_MARK = '-NUMBER-'
        self.TRACE_MARK = '-TRACE-'
        self.COMMAND_MARK = '-COMMAND-'
        self.COMMENT_MARK = '-COMMENT-'
        self.CODE_MARK = '-CODE-'

    def extract_code_from_html_text(self, html_text: str) -> list[str]:
        text_with_code_tag = self.format_line_html_text(html_text)
        has_code_mark = self.CODE_MARK in text_with_code_tag
        if not has_code_mark:
            return []
        code_index_start = 0
        soup = BeautifulSoup(html_text, 'lxml')
        code_tag = soup.find_all(name=['pre', 'blockquote'])
        code_count = text_with_code_tag.count(self.CODE_MARK)
        code_list = []
        for code_index in range(code_index_start, code_index_start + code_count):
            code = code_tag[code_index].get_text()
            if code:
                code_list.append(code)
        return code_list

    def format_line_html_text(self, html_text: str or bytes) -> str:
        soup = BeautifulSoup(html_text, 'lxml')
        code_tag = soup.find_all(['pre', 'blockquote'])
        for tag in code_tag:
            tag.string = self.CODE_MARK
        ul_ol_group = soup.find_all(['ul', 'ol'])
        for ul_ol_item in ul_ol_group:
            li_group = ul_ol_item.find_all('li')
            for li_item in li_group:
                li_item_text = li_item.get_text(strip=True)
                if not li_item_text:
                    continue
                if li_item_text[-1] in string.punctuation:
                    li_item.string = '[-]' + li_item_text
                else:
                    li_item.string = '[-]' + li_item_text + '.'
        p_group = soup.find_all('p')
        for p_item in p_group:
            p_item_text = p_item.get_text(strip=True)
            if p_item_text:
                if p_item_text[-1] in string.punctuation:
                    p_item.string = p_item_text
                    continue
                next_sibling = p_item.next_sibling
                if next_sibling and self.CODE_MARK in next_sibling.get_text():
                    p_item.string = p_item_text + ':'
                    continue
                p_item.string = p_item_text + '.'
        clean_text = soup.get_text()
        clean_text = decode_htmlentities(clean_text)
        return self.__format_line_feed(clean_text)

    def __format_line_feed(self, text: str) -> str:
        # Implementation of line feed normalization
        # This is a private method that normalizes line feeds
        # Based on the specification, it should handle line feed formatting
        # Since no specific implementation is given, we'll do a simple normalization
        return text.replace('\r\n', '\n').replace('\r', '\n')

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
