from urllib.parse import unquote

class UrlPath:
    def __init__(self):
        self.segments = []
        self.trailing_slash = False

    def add(self, segment):
        self.segments.append(self.fix_path(segment))

    def parse(self, path, charset='utf-8'):
        self.trailing_slash = path.endswith('/') if path else False
        path = self.fix_path(path)
        if path:
            self.segments = [unquote(segment, encoding=charset) for segment in path.split('/')]
        else:
            self.segments = []

    @staticmethod
    def fix_path(path):
        return path.strip('/')

import unittest

class UrlPathTestAdd(unittest.TestCase):
    def test_add_1(self):
        url_path = UrlPath()
        url_path.add('foo')
        url_path.add('bar')
        self.assertEqual(url_path.segments, ['foo', 'bar'])

    def test_add_2(self):
        url_path = UrlPath()
        url_path.add('aaa')
        url_path.add('bbb')
        self.assertEqual(url_path.segments, ['aaa', 'bbb'])

    def test_add_3(self):
        url_path = UrlPath()
        url_path.add('123')
        self.assertEqual(url_path.segments, ['123'])

    def test_add_4(self):
        url_path = UrlPath()
        url_path.add('ddd')
        self.assertEqual(url_path.segments, ['ddd'])

    def test_add_5(self):
        url_path = UrlPath()
        url_path.add('eee')
        self.assertEqual(url_path.segments, ['eee'])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
