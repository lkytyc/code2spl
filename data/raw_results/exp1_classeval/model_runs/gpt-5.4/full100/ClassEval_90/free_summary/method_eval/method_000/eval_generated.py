class URLHandler:
    def __init__(self, url):
        self.url = url

    def get_scheme(self):
        separator = "://"
        index = self.url.find(separator)
        if index == -1:
            return None
        return self.url[:index]

    def get_host(self):
        separator = "://"
        index = self.url.find(separator)
        if index == -1:
            return None
        remainder = self.url[index + len(separator):]
        slash_index = remainder.find("/")
        if slash_index == -1:
            return remainder
        return remainder[:slash_index]

    def get_path(self):
        separator = "://"
        index = self.url.find(separator)
        if index == -1:
            return None
        remainder = self.url[index + len(separator):]
        slash_index = remainder.find("/")
        if slash_index == -1:
            return None
        return remainder[slash_index:]

    def get_query_params(self):
        question_index = self.url.find("?")
        if question_index == -1:
            return None
        hash_index = self.url.find("#", question_index + 1)
        if hash_index == -1:
            query_string = self.url[question_index + 1:]
        else:
            query_string = self.url[question_index + 1:hash_index]

        params = {}
        for pair in query_string.split("&"):
            if pair.count("=") == 1:
                key, value = pair.split("=")
                params[key] = value
        return params

    def get_fragment(self):
        hash_index = self.url.find("#")
        if hash_index == -1:
            return None
        return self.url[hash_index + 1:]

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
