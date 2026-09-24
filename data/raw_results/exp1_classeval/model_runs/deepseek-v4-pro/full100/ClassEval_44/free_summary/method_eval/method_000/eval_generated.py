class HtmlTextProcessor:
    def __init__(self):
        import re
        self.re = re

    def format_line_html_text(self, html_text):
        if not html_text:
            return ""
        text = html_text
        text = self.re.sub(r'<pre[^>]*>.*?</pre>', '-CODE-', text, flags=self.re.DOTALL | self.re.IGNORECASE)
        text = self.re.sub(r'<blockquote[^>]*>.*?</blockquote>', '-CODE-', text, flags=self.re.DOTALL | self.re.IGNORECASE)
        text = self.re.sub(r'<li[^>]*>(.*?)</li>', self._format_list_item, text, flags=self.re.DOTALL | self.re.IGNORECASE)
        text = self.re.sub(r'<p[^>]*>(.*?)</p>', self._format_paragraph, text, flags=self.re.DOTALL | self.re.IGNORECASE)
        text = self.re.sub(r'<[^>]+>', '', text)
        text = self.re.sub(r'&nbsp;', ' ', text)
        text = self.re.sub(r'&amp;', '&', text)
        text = self.re.sub(r'&lt;', '<', text)
        text = self.re.sub(r'&gt;', '>', text)
        text = self.re.sub(r'&quot;', '"', text)
        text = self.re.sub(r'&#39;', "'", text)
        text = self.re.sub(r'\n\s*\n+', '\n', text)
        text = text.strip()
        return text

    def _format_list_item(self, match):
        content = match.group(1)
        content = self.re.sub(r'<[^>]+>', '', content)
        content = content.strip()
        if content and not self.re.search(r'[.!?:]$', content):
            content += '.'
        return '[-] ' + content

    def _format_paragraph(self, match):
        content = match.group(1)
        content = self.re.sub(r'<[^>]+>', '', content)
        content = content.strip()
        if not content:
            return ''
        if self.re.search(r'[.!?]$', content):
            return content
        if '-CODE-' in content:
            return content + ':'
        return content + '.'

    def extract_code_from_html_text(self, html_text):
        if not html_text:
            return []
        formatted = self.format_line_html_text(html_text)
        if '-CODE-' not in formatted:
            return []
        code_blocks = []
        for match in self.re.finditer(r'<(pre|blockquote)[^>]*>(.*?)</\1>', html_text, flags=self.re.DOTALL | self.re.IGNORECASE):
            content = match.group(2)
            content = self.re.sub(r'<[^>]+>', '', content)
            content = self.re.sub(r'&nbsp;', ' ', content)
            content = self.re.sub(r'&amp;', '&', content)
            content = self.re.sub(r'&lt;', '<', content)
            content = self.re.sub(r'&gt;', '>', content)
            content = self.re.sub(r'&quot;', '"', content)
            content = self.re.sub(r'&#39;', "'", content)
            code_blocks.append(content.strip())
        return code_blocks

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
