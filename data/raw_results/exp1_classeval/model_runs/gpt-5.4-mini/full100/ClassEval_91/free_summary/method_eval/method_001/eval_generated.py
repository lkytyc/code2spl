class UrlPath:
    def __init__(self):
        self.segments = []
        self.with_end_tag = False

    def add(self, segment):
        self.segments.append(self.fix_path(segment))

    def parse(self, path, charset):
        self.segments = []
        self.with_end_tag = False
        if path and path.endswith("/"):
            self.with_end_tag = True
        path = self.fix_path(path)
        if path == "":
            return
        import urllib.parse
        for segment in path.split("/"):
            self.segments.append(urllib.parse.unquote(segment, encoding=charset))

    @staticmethod
    def fix_path(path):
        if not path:
            return ""
        return path.strip("/")

import unittest

class UrlPathTestParse(unittest.TestCase):
    def test_parse_1(self):
        url_path = UrlPath()
        url_path.parse('/foo/bar/', 'utf-8')
        self.assertEqual(url_path.segments, ['foo', 'bar'])
        self.assertEqual(url_path.with_end_tag, True)

    def test_parse_2(self):
        url_path = UrlPath()
        url_path.parse('aaa/bbb', 'utf-8')
        self.assertEqual(url_path.segments, ['aaa', 'bbb'])
        self.assertEqual(url_path.with_end_tag, False)

    def test_parse_3(self):
        url_path = UrlPath()
        url_path.parse('/123/456/', 'utf-8')
        self.assertEqual(url_path.segments, ['123', '456'])
        self.assertEqual(url_path.with_end_tag, True)

    def test_parse_4(self):
        url_path = UrlPath()
        url_path.parse('/123/456/789', 'utf-8')
        self.assertEqual(url_path.segments, ['123', '456', '789'])
        self.assertEqual(url_path.with_end_tag, False)

    def test_parse_5(self):
        url_path = UrlPath()
        url_path.parse('/foo/bar', 'utf-8')
        self.assertEqual(url_path.segments, ['foo', 'bar'])
        self.assertEqual(url_path.with_end_tag, False)

    def test_parse_6(self):
        url_path = UrlPath()
        url_path.parse('', 'utf-8')
        self.assertEqual(url_path.segments, [])
        self.assertEqual(url_path.with_end_tag, False)

    def test_parse_7(self):
        url_path = UrlPath()
        url_path.parse('//', 'utf-8')
        self.assertEqual(url_path.segments, [])
        self.assertEqual(url_path.with_end_tag, True)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
