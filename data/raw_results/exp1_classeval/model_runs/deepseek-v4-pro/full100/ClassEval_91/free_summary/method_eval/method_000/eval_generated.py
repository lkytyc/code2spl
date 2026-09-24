class UrlPath:
    def __init__(self):
        self.segments = []
        self.with_end_tag = False

    def add(self, segment):
        segment = self.fix_path(segment)
        if segment:
            self.segments.append(segment)

    def parse(self, path, charset):
        if path:
            self.with_end_tag = path.endswith('/')
            path = self.fix_path(path)
            if path:
                parts = path.split('/')
                for part in parts:
                    from urllib.parse import unquote
                    self.segments.append(unquote(part, encoding=charset))

    @staticmethod
    def fix_path(path):
        if not path:
            return ''
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
