import urllib.parse

class UrlPath:
    def __init__(self):
        self.segments = []
        self.with_end_tag = False

    def add(self, segment):
        self.segments.append(segment)

    def parse(self, path, charset):
        self.with_end_tag = path.endswith('/')
        path = self.fix_path(path)
        if path:
            self.segments = [
                urllib.parse.unquote(segment, encoding=charset, errors='replace')
                for segment in path.split('/')
                if segment
            ]
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
