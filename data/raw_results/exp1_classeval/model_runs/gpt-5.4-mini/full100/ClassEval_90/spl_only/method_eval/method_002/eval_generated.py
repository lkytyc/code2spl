class URLHandler:
    def __init__(self, url):
        self.url = url

    def get_scheme(self):
        scheme_end = self.url.find("://")
        if scheme_end != -1:
            return self.url[:scheme_end]
        return None

    def get_host(self):
        scheme_end = self.url.find("://")
        if scheme_end == -1:
            return None
        url_without_scheme = self.url[scheme_end + 3:]
        host_end = url_without_scheme.find("/")
        if host_end != -1:
            return url_without_scheme[:host_end]
        return url_without_scheme

    def get_path(self):
        scheme_end = self.url.find("://")
        if scheme_end == -1:
            return None
        url_without_scheme = self.url[scheme_end + 3:]
        host_end = url_without_scheme.find("/")
        if host_end != -1:
            return url_without_scheme[host_end:]
        return None

    def get_query_params(self):
        query_start = self.url.find("?")
        fragment_start = self.url.find("#")
        if query_start == -1:
            return None

        if fragment_start == -1 or fragment_start < query_start:
            query_string = self.url[query_start + 1:]
        else:
            query_string = self.url[query_start + 1:fragment_start]

        params = {}
        if len(query_string) > 0:
            param_pairs = query_string.split("&")
            for pair in param_pairs:
                key_value = pair.split("=")
                if len(key_value) == 2:
                    key, value = key_value
                    params[key] = value
        return params

    def get_fragment(self):
        fragment_start = self.url.find("#")
        if fragment_start != -1:
            return self.url[fragment_start + 1:]
        return None

import unittest

class URLHandlerTestGetPath(unittest.TestCase):
    def test_get_path_1(self):
        urlhandler = URLHandler("https://www.baidu.com/s?wd=aaa&rsv_spt=1#page")
        temp = urlhandler.get_path()
        self.assertEqual(temp, "/s?wd=aaa&rsv_spt=1#page")

    def test_get_path_2(self):
        urlhandler = URLHandler(
            "https://www.bing.com/search?pglt=41&q=humaneval&cvid=4dc2da2bb4bc429eb498c85245ae5253&aqs=edge.0.0l7j69i61j69i60.10008j0j1&FORM=ANNTA1&PC=U531&mkt=zh-CN")
        temp = urlhandler.get_path()
        self.assertEqual(temp,
                         "/search?pglt=41&q=humaneval&cvid=4dc2da2bb4bc429eb498c85245ae5253&aqs=edge.0.0l7j69i61j69i60.10008j0j1&FORM=ANNTA1&PC=U531&mkt=zh-CN")

    def test_get_path_3(self):
        urlhandler = URLHandler("https://github.com/openai/human-eval")
        temp = urlhandler.get_path()
        self.assertEqual(temp, "/openai/human-eval")

    def test_get_path_4(self):
        urlhandler = URLHandler("https://github.com/aaa/human-eval")
        temp = urlhandler.get_path()
        self.assertEqual(temp, "/aaa/human-eval")

    def test_get_path_5(self):
        urlhandler = URLHandler("https://github.com/bbb/human-eval")
        temp = urlhandler.get_path()
        self.assertEqual(temp, "/bbb/human-eval")

    def test_get_path_6(self):
        urlhandler = URLHandler("abcdefg")
        temp = urlhandler.get_path()
        self.assertIsNone(temp)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
