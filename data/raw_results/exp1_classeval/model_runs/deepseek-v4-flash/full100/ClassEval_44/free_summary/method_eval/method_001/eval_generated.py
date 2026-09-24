from bs4 import BeautifulSoup
import re
import html

class HtmlUtil:
    @staticmethod
    def format_line_html_text(html_text):
        soup = BeautifulSoup(html_text, 'html.parser')
        
        # Replace pre and blockquote with code marker
        for tag in soup.find_all(['pre', 'blockquote']):
            tag.replace_with('<<<CODE>>>')
        
        # Process list items
        for li in soup.find_all('li'):
            text = li.get_text()
            text = text.strip()
            if text:
                if not text.startswith('-'):
                    text = '- ' + text
                if not text.endswith('.'):
                    text += '.'
                li.string = text
        
        # Process paragraphs
        for p in soup.find_all('p'):
            text = p.get_text().strip()
            if text:
                if not text.endswith(('.', ':', ';', '!', '?')):
                    # Check if next sibling is a code marker
                    next_sib = p.find_next_sibling()
                    if next_sib and next_sib.name in ['pre', 'blockquote']:
                        text += ':'
                    else:
                        text += '.'
                p.string = text
        
        # Get text and normalize whitespace
        text = soup.get_text()
        text = html.unescape(text)
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n\s+', '\n', text)
        text = text.strip()
        
        return text
    
    @staticmethod
    def extract_code_from_html_text(html_text):
        soup = BeautifulSoup(html_text, 'html.parser')
        code_blocks = []
        for tag in soup.find_all(['pre', 'blockquote']):
            code_blocks.append(tag.get_text())
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
