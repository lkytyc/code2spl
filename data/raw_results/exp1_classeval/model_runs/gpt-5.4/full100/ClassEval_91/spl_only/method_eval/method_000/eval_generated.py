class UrlPath:
    def __init__(self):
        self.segments = []
        self.with_end_tag = False

    def add(self, segment):
        normalized_segment = self.fix_path(segment)
        self.segments.append(normalized_segment)

    def parse(self, path, charset):
        import urllib.parse

        if path:
            if path.endswith('/'):
                self.with_end_tag = True
            path = self.fix_path(path)
            if path:
                for seg in path.split('/'):
                    decoded_seg = urllib.parse.unquote(seg, encoding=charset)
                    self.segments.append(decoded_seg)

    def fix_path(self, path):
        if not path:
            return ""
        segment_str = path.strip('/')
        return segment_str

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
