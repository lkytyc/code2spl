class URLHandler:
    def __init__(self, url):
        self.url = url

    def get_scheme(self):
        idx = self.url.find("://")
        if idx == -1:
            return None
        return self.url[:idx]

    def get_host(self):
        idx = self.url.find("://")
        if idx == -1:
            return None
        remainder = self.url[idx + 3:]
        slash_idx = remainder.find("/")
        if slash_idx == -1:
            return remainder
        return remainder[:slash_idx]

    def get_path(self):
        idx = self.url.find("://")
        if idx == -1:
            return None
        remainder = self.url[idx + 3:]
        slash_idx = remainder.find("/")
        if slash_idx == -1:
            return None
        return remainder[slash_idx:]

    def get_query_params(self):
        q_idx = self.url.find("?")
        if q_idx == -1:
            return None
        hash_idx = self.url.find("#", q_idx + 1)
        if hash_idx == -1:
            query_string = self.url[q_idx + 1:]
        else:
            query_string = self.url[q_idx + 1:hash_idx]

        params = {}
        if query_string == "":
            return params

        for pair in query_string.split("&"):
            if pair.count("=") == 1:
                key, value = pair.split("=")
                params[key] = value
        return params

    def get_fragment(self):
        idx = self.url.find("#")
        if idx == -1:
            return None
        return self.url[idx + 1:]

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
