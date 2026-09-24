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
