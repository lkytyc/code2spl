class URLHandler:
    def __init__(self, url):
        self.url = url

    def get_scheme(self):
        if "://" not in self.url:
            return None
        return self.url.split("://", 1)[0]

    def get_host(self):
        if "://" not in self.url:
            return None
        rest = self.url.split("://", 1)[1]
        if "/" in rest:
            return rest.split("/", 1)[0]
        return rest

    def get_path(self):
        if "://" not in self.url:
            return None
        rest = self.url.split("://", 1)[1]
        if "/" not in rest:
            return None
        path = "/" + rest.split("/", 1)[1]
        if "?" in path:
            path = path.split("?", 1)[0]
        if "#" in path:
            path = path.split("#", 1)[0]
        return path

    def get_query_params(self):
        if "?" not in self.url:
            return None
        query_part = self.url.split("?", 1)[1]
        if "#" in query_part:
            query_part = query_part.split("#", 1)[0]
        params = {}
        for pair in query_part.split("&"):
            if "=" in pair and pair.count("=") == 1:
                key, value = pair.split("=", 1)
                params[key] = value
        return params

    def get_fragment(self):
        if "#" not in self.url:
            return None
        return self.url.split("#", 1)[1]

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
