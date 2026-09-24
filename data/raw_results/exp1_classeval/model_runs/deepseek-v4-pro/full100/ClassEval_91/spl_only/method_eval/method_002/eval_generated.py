import urllib.parse


class UrlPath:
    def __init__(self):
        self.segments = []
        self.with_end_tag = False

    def add(self, segment):
        normalized_segment = self.fix_path(segment)
        self.segments.append(normalized_segment)

    def parse(self, path, charset):
        if path:
            if path.endswith('/'):
                self.with_end_tag = True
            path = self.fix_path(path)
            if path:
                split = path.split('/')
                for seg in split:
                    decoded_seg = urllib.parse.unquote(seg, encoding=charset)
                    self.segments.append(decoded_seg)

    def fix_path(self, path):
        if not path:
            return ''
        segment_str = path.strip('/')
        return segment_str

import unittest

class UrlPathTestFixPath(unittest.TestCase):
    def test_fix_path_1(self):
        fixed_path = UrlPath.fix_path('/foo/bar/')
        self.assertEqual(fixed_path, 'foo/bar')

    def test_fix_path_2(self):
        fixed_path = UrlPath.fix_path('/aaa/bbb/')
        self.assertEqual(fixed_path, 'aaa/bbb')

    def test_fix_path_3(self):
        fixed_path = UrlPath.fix_path('/a/b/')
        self.assertEqual(fixed_path, 'a/b')

    def test_fix_path_4(self):
        fixed_path = UrlPath.fix_path('/111/222/')
        self.assertEqual(fixed_path, '111/222')

    def test_fix_path_5(self):
        fixed_path = UrlPath.fix_path('/a/')
        self.assertEqual(fixed_path, 'a')

    def test_fix_path_6(self):
        fixed_path = UrlPath.fix_path('')
        self.assertEqual(fixed_path, '')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
