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
        normalized_segment = self.fix_path(segment)
        self.segments.append(normalized_segment)

    def parse(self, path, charset):
        """
        Parses a given path string and populates the list of segments in the UrlPath.
        :param path: str, the path string to parse.
        :param charset: str, the character encoding of the path string.
        >>> url_path = UrlPath()
        >>> url_path.parse('/foo/bar/', 'utf-8')

        url_path.segments = ['foo', 'bar']
        """
        if path:
            if path.endswith('/'):
                self.with_end_tag = True
            path = self.fix_path(path)
            if path:
                split = path.split('/')
                for seg in split:
                    decoded_seg = urllib.parse.unquote(seg, encoding=charset)
                    self.segments.append(decoded_seg)

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
        if path:
            segment_str = path.strip('/')
            return segment_str
        return ""

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
