from urllib.parse import urlparse, parse_qs, urlunparse


class URLHandler:
    """
    The class supports to handle URLs, including extracting the scheme, host, path, query parameters, and fragment.
    """

    def __init__(self, url):
        """
        Initialize URLHandler's URL
        """
        self.url = url

    def get_scheme(self):
        """
        get the scheme of the URL
        :return: string, If successful, return the scheme of the URL
        >>> urlhandler = URLHandler("https://www.baidu.com/s?wd=aaa&rsv_spt=1#page")
        >>> urlhandler.get_scheme()
        "https"
        """
        parsed = urlparse(self.url)
        return parsed.scheme

    def get_host(self):
        """
        Get the second part of the URL, which is the host domain name
        :return: string, If successful, return the host domain name of the URL
        >>> urlhandler = URLHandler("https://www.baidu.com/s?wd=aaa&rsv_spt=1#page")
        >>> urlhandler.get_host()
        "www.baidu.com"
        """
        parsed = urlparse(self.url)
        return parsed.netloc

    def get_path(self):
        """
        Get the third part of the URL, which is the address of the resource
        :return: string, If successful, return the address of the resource of the URL
        >>> urlhandler = URLHandler("https://www.baidu.com/s?wd=aaa&rsv_spt=1#page")
        >>> urlhandler.get_path()
        "/s?wd=aaa&rsv_spt=1#page"
        """
        parsed = urlparse(self.url)
        path = parsed.path
        if parsed.query:
            path += '?' + parsed.query
        if parsed.fragment:
            path += '#' + parsed.fragment
        return path

    def get_query_params(self):
        """
        Get the request parameters for the URL
        :return: dict, If successful, return the request parameters of the URL
        >>> urlhandler = URLHandler("https://www.baidu.com/s?wd=aaa&rsv_spt=1#page")
        >>> urlhandler.get_query_params()
        {"wd": "aaa", "rsv_spt": "1"}
        """
        parsed = urlparse(self.url)
        params = parse_qs(parsed.query)
        # parse_qs returns lists for each value; flatten to single values
        return {key: values[0] for key, values in params.items()}

    def get_fragment(self):
        """
        Get the fragment after '#' in the URL
        :return: string, If successful, return the fragment after '#' of the URL
        >>> urlhandler = URLHandler("https://www.baidu.com/s?wd=aaa&rsv_spt=1#page")
        >>> urlhandler.get_fragment()
        "page"
        """
        parsed = urlparse(self.url)
        return parsed.fragment

import unittest

class URLHandlerTestGetQueryParams(unittest.TestCase):
    def test_get_query_params_1(self):
        urlhandler = URLHandler("https://www.baidu.com/s?wd=aaa&rsv_spt=1#page")
        temp = urlhandler.get_query_params()
        self.assertEqual(temp, {"wd": "aaa", "rsv_spt": "1"})

    def test_get_query_params_2(self):
        urlhandler = URLHandler(
            "https://www.bing.com/search?pglt=41&q=humaneval&cvid=4dc2da2bb4bc429eb498c85245ae5253&aqs=edge.0.0l7j69i61j69i60.10008j0j1&FORM=ANNTA1&PC=U531#")
        temp = urlhandler.get_query_params()
        self.assertEqual(temp, {"pglt": "41", "q": "humaneval", "cvid": "4dc2da2bb4bc429eb498c85245ae5253",
                                "aqs": "edge.0.0l7j69i61j69i60.10008j0j1", "FORM": "ANNTA1", "PC": "U531"})

    def test_get_query_params_3(self):
        urlhandler = URLHandler("https://github.com/openai/human-eval")
        temp = urlhandler.get_query_params()
        self.assertEqual(temp, None)

    def test_get_query_params_4(self):
        urlhandler = URLHandler("https://www.baidu.com/s?wd=bbb&rsv_spt=1#page")
        temp = urlhandler.get_query_params()
        self.assertEqual(temp, {"wd": "bbb", "rsv_spt": "1"})

    def test_get_query_params_5(self):
        urlhandler = URLHandler("https://www.baidu.com/s?wd=ccc&rsv_spt=1#page")
        temp = urlhandler.get_query_params()
        self.assertEqual(temp, {"wd": "ccc", "rsv_spt": "1"})

    def test_get_query_params_6(self):
        urlhandler = URLHandler("https://www.baidu.com/s?&#page")
        temp = urlhandler.get_query_params()
        self.assertEqual(temp, {})

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
