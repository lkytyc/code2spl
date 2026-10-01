import string
import gensim.utils
from bs4 import BeautifulSoup


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

    def __format_line_feed(self, text):
        lines = text.split('\n')
        result = []
        for line in lines:
            line = line.strip()
            if line:
                result.append(line)
        return '\n'.join(result)

    def extract_code_from_html_text(self, html_text):
        text_with_code_tag = self.format_line_html_text(html_text)
        code_index_start = 0
        soup = BeautifulSoup(html_text, 'lxml')
        code_tag = soup.find_all(['pre', 'blockquote'])
        code_count = text_with_code_tag.count(self.CODE_MARK)
        code_list = []
        if not code_count:
            return code_list
        for code_index in range(code_index_start, code_index_start + code_count):
            code = code_tag[code_index].get_text()
            if code:
                code_list.append(code)
        return code_list

    def format_line_html_text(self, html_text):
        if html_text is None or len(html_text) == 0:
            return ''

        soup = BeautifulSoup(html_text, 'lxml')

        code_tag = soup.find_all(['pre', 'blockquote'])
        for tag in code_tag:
            tag.string = self.CODE_MARK

        ul_ol_group = soup.find_all(['ul', 'ol'])
        for ul_ol_item in ul_ol_group:
            li_group = ul_ol_item.find_all('li')
            for li_item in li_group:
                li_item_text = li_item.get_text().strip()
                if len(li_item_text) == 0:
                    continue
                if li_item_text[-1] in string.punctuation:
                    li_item.string = '[-]' + li_item_text
                    continue
                li_item.string = '[-]' + li_item_text + '.'

        p_group = soup.find_all('p')
        for p_item in p_group:
            p_item_text = p_item.get_text().strip()
            if not p_item_text:
                continue
            if p_item_text[-1] in string.punctuation:
                p_item.string = p_item_text
                continue
            next_sibling = p_item.find_next_sibling()
            if next_sibling is not None and self.CODE_MARK in next_sibling.get_text():
                p_item.string = p_item_text + ':'
                continue
            p_item.string = p_item_text + '.'

        clean_text = gensim.utils.decode_htmlentities(soup.get_text())
        return self.__format_line_feed(clean_text)

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
