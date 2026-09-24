class HtmlUtil:
    def __init__(self):
        self.code_marker = "__HTML_UTIL_CODE_MARKER__"
        self.p_marker = "__HTML_UTIL_P_MARKER__"
        self.li_marker = "__HTML_UTIL_LI_MARKER__"
        self.br_marker = "__HTML_UTIL_BR_MARKER__"

    def format_line_html_text(self, html_text):
        if html_text is None or html_text == "":
            return ""

        from bs4 import BeautifulSoup
        import html as html_module
        import re

        soup = BeautifulSoup(html_text, "lxml")

        for tag_name in ("pre", "blockquote"):
            for tag in soup.find_all(tag_name):
                tag.clear()
                tag.append(self.code_marker)

        def has_terminal_punct(text):
            text = (text or "").rstrip()
            return bool(text) and text[-1] in ".!?;:，。！？；："

        for list_tag in soup.find_all(["ul", "ol"]):
            for li in list_tag.find_all("li", recursive=False):
                text = li.get_text(" ", strip=True)
                if not text:
                    li.decompose()
                    continue
                text = text.strip()
                if not has_terminal_punct(text):
                    text += "."
                li.clear()
                li.append("[-] " + text)

        for p in soup.find_all("p"):
            text = p.get_text(" ", strip=True)
            if not text:
                p.decompose()
                continue

            if has_terminal_punct(text):
                new_text = text
            else:
                next_sibling = p.find_next_sibling()
                if next_sibling is not None and self.code_marker in next_sibling.get_text(" ", strip=True):
                    new_text = text + ":"
                else:
                    new_text = text + "."

            p.clear()
            p.append(new_text)

        text = soup.get_text("\n")
        text = html_module.unescape(text)
        text = re.sub(r"\n{2,}", "\n", text)
        return text.strip()

    def extract_code_from_html_text(self, html_text):
        if html_text is None or html_text == "":
            return []

        formatted_text = self.format_line_html_text(html_text)
        if self.code_marker not in formatted_text:
            return []

        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html_text, "lxml")
        code_sections = []
        for tag_name in ("pre", "blockquote"):
            for tag in soup.find_all(tag_name):
                code_sections.append(tag.get_text("\n", strip=True))
        return code_sections

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
