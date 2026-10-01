class URLHandler:
    def __init__(self, url):
        self.url = url

    def get_fragment(self):
        fragment_start = self.url.find('#')
        if fragment_start != -1:
            return self.url[fragment_start + 1:]
        return None

    def get_host(self):
        scheme_end = self.url.find('://')
        if scheme_end != -1:
            url_without_scheme = self.url[scheme_end + 3:]
            host_end = url_without_scheme.find('/')
            if host_end != -1:
                return url_without_scheme[:host_end]
            else:
                return url_without_scheme
        return None

    def get_path(self):
        scheme_end = self.url.find('://')
        if scheme_end != -1:
            url_without_scheme = self.url[scheme_end + 3:]
            host_end = url_without_scheme.find('/')
            if host_end != -1:
                return url_without_scheme[host_end:]
        return None

    def get_query_params(self):
        query_start = self.url.find('?')
        fragment_start = self.url.find('#')
        if query_start != -1:
            if fragment_start != -1:
                query_string = self.url[query_start + 1:fragment_start]
            else:
                query_string = self.url[query_start + 1:]
            params = {}
            if len(query_string) > 0:
                param_pairs = query_string.split('&')
                for pair in param_pairs:
                    key_value = pair.split('=')
                    if len(key_value) == 2:
                        key, value = key_value
                        params[key] = value
            return params
        return None

    def get_scheme(self):
        scheme_end = self.url.find('://')
        if scheme_end != -1:
            return self.url[:scheme_end]
        return None

import unittest

class URLHandlerTestGetFragment(unittest.TestCase):
    def test_get_fragment_1(self):
        urlhandler = URLHandler("https://www.baidu.com/s?wd=aaa&rsv_spt=1#page")
        temp = urlhandler.get_fragment()
        self.assertEqual(temp, "page")

    def test_get_fragment_2(self):
        urlhandler = URLHandler(
            "https://www.bing.com/search?pglt=41&q=humaneval&cvid=4dc2da2bb4bc429eb498c85245ae5253&aqs=edge.0.0l7j69i61j69i60.10008j0j1&FORM=ANNTA1&PC=U531&mkt=zh-CN")
        temp = urlhandler.get_fragment()
        self.assertEqual(temp, None)

    def test_get_fragment_3(self):
        urlhandler = URLHandler("https://www.baidu.com/s?wd=aaa&rsv_spt=1#aaa")
        temp = urlhandler.get_fragment()
        self.assertEqual(temp, "aaa")

    def test_get_fragment_4(self):
        urlhandler = URLHandler("https://www.baidu.com/s?wd=aaa&rsv_spt=1#bbb")
        temp = urlhandler.get_fragment()
        self.assertEqual(temp, "bbb")

    def test_get_fragment_5(self):
        urlhandler = URLHandler("https://www.baidu.com/s?wd=aaa&rsv_spt=1#ccc")
        temp = urlhandler.get_fragment()
        self.assertEqual(temp, "ccc")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
