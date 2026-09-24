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
        return self.url.split("://")[0]

    def get_host(self):
        """
        Get the second part of the URL, which is the host domain name
        :return: string, If successful, return the host domain name of the URL
        >>> urlhandler = URLHandler("https://www.baidu.com/s?wd=aaa&rsv_spt=1#page")
        >>> urlhandler.get_host()
        "www.baidu.com"
        """
        temp = self.url.split("://")[1]
        return temp.split("/")[0]

    def get_path(self):
        """
        Get the third part of the URL, which is the address of the resource
        :return: string, If successful, return the address of the resource of the URL
        >>> urlhandler = URLHandler("https://www.baidu.com/s?wd=aaa&rsv_spt=1#page")
        >>> urlhandler.get_path()
        "/s?wd=aaa&rsv_spt=1#page"
        """
        temp = self.url.split("://")[1]
        return "/" + temp.split("/", 1)[1] if "/" in temp else ""

    def get_query_params(self):
        """
        Get the request parameters for the URL
        :return: dict, If successful, return the request parameters of the URL
        >>> urlhandler = URLHandler("https://www.baidu.com/s?wd=aaa&rsv_spt=1#page")
        >>> urlhandler.get_query_params()
        {"wd": "aaa", "rsv_spt": "1"}
        """
        if "?" not in self.url:
            return {}
        query_string = self.url.split("?")[1].split("#")[0]
        params = {}
        for pair in query_string.split("&"):
            if "=" in pair:
                key, value = pair.split("=", 1)
                params[key] = value
        return params

    def get_fragment(self):
        """
        Get the fragment after '#' in the URL
        :return: string, If successful, return the fragment after '#' of the URL
        >>> urlhandler = URLHandler("https://www.baidu.com/s?wd=aaa&rsv_spt=1#page")
        >>> urlhandler.get_fragment()
        "page"
        """
        if "#" in self.url:
            return self.url.split("#")[1]
        return ""

import unittest

class URLHandlerTestGetHost(unittest.TestCase):
    def test_get_host_1(self):
        urlhandler = URLHandler("https://www.baidu.com/s?wd=aaa&rsv_spt=1#page")
        temp = urlhandler.get_host()
        self.assertEqual(temp, "www.baidu.com")

    def test_get_host_2(self):
        urlhandler = URLHandler(
            "https://www.bing.com/search?pglt=41&q=humaneval&cvid=4dc2da2bb4bc429eb498c85245ae5253&aqs=edge.0.0l7j69i61j69i60.10008j0j1&FORM=ANNTA1&PC=U531&mkt=zh-CN")
        temp = urlhandler.get_host()
        self.assertEqual(temp, "www.bing.com")

    def test_get_host_3(self):
        urlhandler = URLHandler("https://github.com/openai/human-eval")
        temp = urlhandler.get_host()
        self.assertEqual(temp, "github.com")

    def test_get_host_4(self):
        urlhandler = URLHandler("https://aaa.com/openai/human-eval")
        temp = urlhandler.get_host()
        self.assertEqual(temp, "aaa.com")

    def test_get_host_5(self):
        urlhandler = URLHandler("https://bbb.com/openai/human-eval")
        temp = urlhandler.get_host()
        self.assertEqual(temp, "bbb.com")

    def test_get_host_6(self):
        urlhandler = URLHandler("abcdefg")
        temp = urlhandler.get_host()
        self.assertIsNone(temp)

    def test_get_host_7(self):
        urlhandler = URLHandler("https://bbb.com")
        temp = urlhandler.get_host()
        self.assertEqual(temp, "bbb.com")

    def test_get_host_8(self):
        urlhandler = URLHandler("https://bbb.com/")
        temp = urlhandler.get_host()
        self.assertEqual(temp, "bbb.com")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
