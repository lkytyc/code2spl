class URLHandler:
    def __init__(self, url):
        self.url = url

    def get_scheme(self):
        sep = "://"
        i = self.url.find(sep)
        return None if i == -1 else self.url[:i]

    def get_host(self):
        sep = "://"
        i = self.url.find(sep)
        if i == -1:
            return None
        rest = self.url[i + len(sep):]
        j = rest.find("/")
        return rest if j == -1 else rest[:j]

    def get_path(self):
        sep = "://"
        i = self.url.find(sep)
        if i == -1:
            return None
        rest = self.url[i + len(sep):]
        j = rest.find("/")
        return None if j == -1 else rest[j:]

    def get_query_params(self):
        i = self.url.find("?")
        if i == -1:
            return None
        query = self.url[i + 1:]
        if query == "":
            return {}
        params = {}
        for part in query.split("&"):
            if "=" in part:
                key, value = part.split("=", 1)
            else:
                key, value = part, ""
            params[key] = value
        return params

    def get_fragment(self):
        i = self.url.find("#")
        return None if i == -1 else self.url[i + 1:]

import unittest

class URLHandlerTestGetScheme(unittest.TestCase):
    def test_get_scheme_1(self):
        urlhandler = URLHandler("https://www.baidu.com/s?wd=aaa&rsv_spt=1#page")
        temp = urlhandler.get_scheme()
        self.assertEqual(temp, "https")

    def test_get_scheme_2(self):
        urlhandler = URLHandler(
            "https://www.bing.com/search?pglt=41&q=humaneval&cvid=4dc2da2bb4bc429eb498c85245ae5253&aqs=edge.0.0l7j69i61j69i60.10008j0j1&FORM=ANNTA1&PC=U531&mkt=zh-CN")
        temp = urlhandler.get_scheme()
        self.assertEqual(temp, "https")

    def test_get_scheme_3(self):
        urlhandler = URLHandler("https://github.com/openai/human-eval")
        temp = urlhandler.get_scheme()
        self.assertEqual(temp, "https")

    def test_get_scheme_4(self):
        urlhandler = URLHandler("aaa://github.com/openai/human-eval")
        temp = urlhandler.get_scheme()
        self.assertEqual(temp, "aaa")

    def test_get_scheme_5(self):
        urlhandler = URLHandler("bbb://github.com/openai/human-eval")
        temp = urlhandler.get_scheme()
        self.assertEqual(temp, "bbb")

    def test_get_scheme_6(self):
        urlhandler = URLHandler("abcdefg")
        temp = urlhandler.get_scheme()
        self.assertIsNone(temp)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
