import urllib.parse

class UrlPath:
    """
    The  class is a utility for encapsulating and manipulating the path component of a URL, including adding nodes, parsing path strings, and building path strings with optional encoding.
    """

    def __init__(self):
        """
        Initializes the UrlPath object with an empty list of segments and a flag indicating the presence of an end tag.
        """
        self.segments = []
        self.with_end_tag = False

    def add(self, segment):
        """
        Adds a segment to the list of segments in the UrlPath.
        :param segment: str, the segment to add.
        >>> url_path = UrlPath()
        >>> url_path.add('foo')
        >>> url_path.add('bar')

        url_path.segments = ['foo', 'bar']
        """
        self.segments.append(segment)

    def parse(self, path, charset):
        """
        Parses a given path string and populates the list of segments in the UrlPath.
        :param path: str, the path string to parse.
        :param charset: str, the character encoding of the path string.
        >>> url_path = UrlPath()
        >>> url_path.parse('/foo/bar/', 'utf-8')

        url_path.segments = ['foo', 'bar']
        """
        if path is None:
            self.segments = []
            self.with_end_tag = False
            return
        path = self.fix_path(path)
        if path == "":
            self.segments = []
            self.with_end_tag = str(path).endswith("/")
            return
        parts = path.split("/")
        self.segments = [urllib.parse.unquote(part, encoding=charset, errors="replace") for part in parts if part != ""]
        self.with_end_tag = str(path).endswith("/")

    @staticmethod
    def fix_path(path):
        """
        Fixes the given path string by removing leading and trailing slashes.
        :param path: str, the path string to fix.
        :return: str, the fixed path string.
        >>> url_path = UrlPath()
        >>> url_path.fix_path('/foo/bar/')
        'foo/bar'

        """
        if path is None:
            return None
        start = 0
        end = len(path)
        while start < end and path[start] == "/":
            start += 1
        while end > start and path[end - 1] == "/":
            end -= 1
        return path[start:end]

    def build(self, charset, encode):
        """
        Builds the path string from segments.
        :param charset: str, encoding charset
        :param encode: bool, whether to URL-encode each segment
        :return: str
        """
        if encode:
            parts = [urllib.parse.quote(segment, encoding=charset, safe="") for segment in self.segments]
        else:
            parts = list(self.segments)
        path = "/".join(parts)
        if self.with_end_tag and path != "":
            path += "/"
        return path

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
