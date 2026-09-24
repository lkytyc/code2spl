import re
import string
import gensim
from bs4 import BeautifulSoup

class HtmlUtil:
    """
    This is a class as util for html, supporting for formatting and extracting code from HTML text, including cleaning up the text and converting certain elements into specific marks.
    """

    def __init__(self):
        """
        Initialize a series of labels
        """
        self.SPACE_MARK = '-SPACE-'
        self.JSON_MARK = '-JSON-'
        self.MARKUP_LANGUAGE_MARK = '-MARKUP_LANGUAGE-'
        self.URL_MARK = '-URL-'
        self.NUMBER_MARK = '-NUMBER-'
        self.TRACE_MARK = '-TRACE-'
        self.COMMAND_MARK = '-COMMAND-'
        self.COMMENT_MARK = '-COMMENT-'
        self.CODE_MARK = '-CODE-'

    @staticmethod
    def __format_line_feed(text):
        """
        Replace consecutive line breaks with a single line break
        :param text: string with consecutive line breaks
        :return:string, replaced text with single line break
        """
        return re.sub(r'\n+', '\n', text)

    def format_line_html_text(self, html_text):
        """
        get the html text without the code, and add the code tag -CODE- where the code is
        :param html_text:string
        :return:string
        """
        soup = BeautifulSoup(html_text, 'html.parser')

        # Replace all <pre> blocks (with or without nested <code>) with the CODE_MARK
        for pre in soup.find_all('pre'):
            pre.replace_with(self.CODE_MARK)

        # Get the text, using newline as separator between block elements
        text = soup.get_text(separator='\n')

        # Clean up consecutive blank lines
        text = self.__format_line_feed(text)

        # Strip leading/trailing whitespace from each line and remove empty lines
        lines = [line.strip() for line in text.splitlines()]
        lines = [line for line in lines if line]

        return '\n'.join(lines)

    def extract_code_from_html_text(self, html_text):
        """
        extract codes from the html body
        :param html_text: string, html text
        :return: the list of code
        """
        soup = BeautifulSoup(html_text, 'html.parser')
        codes = []

        for pre in soup.find_all('pre'):
            # If the <pre> contains a <code> tag, get its text; otherwise get the pre text directly
            code_tag = pre.find('code')
            if code_tag:
                codes.append(code_tag.get_text())
            else:
                codes.append(pre.get_text())

        return codes

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
