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

class HtmlUtilTestExtractCodeFromHtmlText(unittest.TestCase):
    def test_extract_code_from_html_text_1(self):
        htmlutil = HtmlUtil()
        res = htmlutil.extract_code_from_html_text('''
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
        self.assertEqual(res, ["print('Hello, world!')", 'for i in range(5):\n                print(i)'])

    def test_extract_code_from_html_text_2(self):
        htmlutil = HtmlUtil()
        res = htmlutil.extract_code_from_html_text('''
                <html>
                <body>
                <h1>Title</h1>
                <p>This is a paragraph.</p>
                <pre>print('Hello, world!')</pre>
                <p>Another paragraph.</p>
                <pre><code>for i in range(4):
                print(i)</code></pre>
                </body>
                </html>
                ''')
        self.assertEqual(res, ["print('Hello, world!')", 'for i in range(4):\n                print(i)'])

    def test_extract_code_from_html_text_3(self):
        htmlutil = HtmlUtil()
        res = htmlutil.extract_code_from_html_text('''
                <html>
                <body>
                <h1>Title</h1>
                <p>This is a paragraph.</p>
                <pre>print('Hello, world!')</pre>
                <p>Another paragraph.</p>
                <pre><code>for i in range(3):
                print(i)</code></pre>
                </body>
                </html>
                ''')
        self.assertEqual(res, ["print('Hello, world!')", 'for i in range(3):\n                print(i)'])

    def test_extract_code_from_html_text_4(self):
        htmlutil = HtmlUtil()
        res = htmlutil.extract_code_from_html_text('''
                <html>
                <body>
                <h1>Title</h1>
                <p>This is a paragraph.</p>
                <pre>print('Hello, world!')</pre>
                <p>Another paragraph.</p>
                <pre><code>for i in range(2):
                print(i)</code></pre>
                </body>
                </html>
                ''')
        self.assertEqual(res, ["print('Hello, world!')", 'for i in range(2):\n                print(i)'])

    def test_extract_code_from_html_text_5(self):
        htmlutil = HtmlUtil()
        htmlutil.CODE_MARK = 'abcdefg'
        res = htmlutil.extract_code_from_html_text("")
        self.assertEqual(res, [])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
