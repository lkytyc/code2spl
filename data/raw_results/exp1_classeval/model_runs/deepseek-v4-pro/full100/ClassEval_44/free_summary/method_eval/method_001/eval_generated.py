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

class HtmlUtilTestFormatLineHtmlText(unittest.TestCase):
    def test_format_line_html_text_1(self):
        htmlutil = HtmlUtil()
        res = htmlutil.format_line_html_text('''
        <html>
        <body>
        <h1>Title</h1>
        <p>This is a paragraph.</p>
        <pre>print('Hello, world!')</pre>
        <p>Another paragraph.</p>
        <pre><code>for i in range(5):
        print(i)</code></pre>
        </body>
        </html>
        ''')
        self.assertEqual(res, '''
Title
This is a paragraph.
-CODE-
Another paragraph.
-CODE-
''')

    def test_format_line_html_text_2(self):
        htmlutil = HtmlUtil()
        res = htmlutil.format_line_html_text('''
        <html>
        <body>
        <h1>Title2</h1>
        <p>This is a paragraph.</p>
        <pre>print('Hello, world!')</pre>
        <p>Another paragraph.</p>
        <pre><code>for i in range(5):
        print(i)</code></pre>
        </body>
        </html>
        ''')
        self.assertEqual(res, '''
Title2
This is a paragraph.
-CODE-
Another paragraph.
-CODE-
''')

    def test_format_line_html_text_3(self):
        htmlutil = HtmlUtil()
        res = htmlutil.format_line_html_text('''
        <html>
        <body>
        <h1>Title3</h1>
        <p>This is a paragraph.</p>
        <pre>print('Hello, world!')</pre>
        <p>Another paragraph.</p>
        <pre><code>for i in range(5):
        print(i)</code></pre>
        </body>
        </html>
        ''')
        self.assertEqual(res, '''
Title3
This is a paragraph.
-CODE-
Another paragraph.
-CODE-
''')

    def test_format_line_html_text_4(self):
        htmlutil = HtmlUtil()
        res = htmlutil.format_line_html_text('''
        <html>
        <body>
        <h1>Title4</h1>
        <p>This is a paragraph.</p>
        <pre>print('Hello, world!')</pre>
        <p>Another paragraph.</p>
        <pre><code>for i in range(5):
        print(i)</code></pre>
        </body>
        </html>
        ''')
        self.assertEqual(res, '''
Title4
This is a paragraph.
-CODE-
Another paragraph.
-CODE-
''')

    def test_format_line_html_text_5(self):
        htmlutil = HtmlUtil()
        res = htmlutil.format_line_html_text('''
        <html>
        <body>
        <h1>Title5</h1>
        <p>This is a paragraph.</p>
        <pre>print('Hello, world!')</pre>
        <p>Another paragraph.</p>
        <pre><code>for i in range(5):
        print(i)</code></pre>
        </body>
        </html>
        ''')
        self.assertEqual(res, '''
Title5
This is a paragraph.
-CODE-
Another paragraph.
-CODE-
''')
    def test_format_line_html_text_6(self):
        htmlutil = HtmlUtil()
        res = htmlutil.format_line_html_text('')
        self.assertEqual(res, '')

    def test_format_line_html_text_7(self):
        htmlutil = HtmlUtil()
        res = htmlutil.format_line_html_text('''<ul><li>Item 1!</li></ul>''')
        self.assertEqual(res, '''[-]Item 1!''')

    def test_format_line_html_text_8(self):
        htmlutil = HtmlUtil()
        res = htmlutil.format_line_html_text('''<ul><li></li></ul>''')
        self.assertEqual(res, '')

    def test_format_line_html_text_9(self):
        htmlutil = HtmlUtil()
        res = htmlutil.format_line_html_text('''<p>Some sentence here.</p>''')
        self.assertEqual(res, 'Some sentence here.')

    def test_format_line_html_text_10(self):
        htmlutil = HtmlUtil()
        res = htmlutil.format_line_html_text('''<p>Some paragraph here</p><code>Code block</code>''')
        self.assertEqual(res, '''Some paragraph here.Code block''')

    def test_format_line_html_text_11(self):
        htmlutil = HtmlUtil()
        res = htmlutil.format_line_html_text('''<p>Some paragraph here</p><div>Some text here</div>''')
        self.assertEqual(res, '''Some paragraph here.Some text here''')

    def test_format_line_html_text_12(self):
        htmlutil = HtmlUtil()
        res = htmlutil.format_line_html_text('''<ul><li>Item 1</li></ul>''')
        self.assertEqual(res, '''[-]Item 1.''')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
