import re
import string
from bs4 import BeautifulSoup
from gensim.utils import decode_htmlentities


class HtmlUtil:
    def __init__(self):
        self.CODE_MARK = "-CODE-"

    @staticmethod
    def __format_line_feed(text):
        if not text:
            return ""
        text = re.sub(r"\n+", "\n", text)
        return text.strip()

    def format_line_html_text(self, html_text):
        if not html_text:
            return ""

        soup = BeautifulSoup(html_text, "lxml")

        for tag in soup.find_all(["pre", "blockquote"]):
            tag.clear()
            tag.append(self.CODE_MARK)

        for list_tag in soup.find_all(["ul", "ol"]):
            for li in list_tag.find_all("li"):
                item_text = li.get_text(" ", strip=True)
                if item_text and item_text[-1] not in string.punctuation:
                    item_text += "."
                li.clear()
                li.append(f"[-]{item_text}")

        for p in soup.find_all("p"):
            paragraph_text = p.get_text(" ", strip=True)
            if not paragraph_text:
                continue

            next_tag = p.find_next_sibling()
            ends_with_code = False
            while next_tag is not None:
                if getattr(next_tag, "name", None) is not None:
                    next_text = next_tag.get_text(" ", strip=True)
                    if next_text == self.CODE_MARK:
                        ends_with_code = True
                    break
                next_tag = next_tag.find_next_sibling()

            if paragraph_text[-1] not in string.punctuation:
                paragraph_text += ":" if ends_with_code else "."

            p.clear()
            p.append(paragraph_text)

        text = soup.get_text("\n")
        text = decode_htmlentities(text)
        text = self.__format_line_feed(text)
        return text

    def extract_code_from_html_text(self, html_text):
        formatted_text = self.format_line_html_text(html_text)
        if self.CODE_MARK not in formatted_text:
            return []

        soup = BeautifulSoup(html_text, "lxml")
        code_blocks = []
        for tag in soup.find_all(["pre", "blockquote"]):
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
