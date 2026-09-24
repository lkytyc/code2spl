class URLHandler:
    def __init__(self, url: str):
        self._url = url

    def get_scheme(self) -> str | None:
        sep = "://"
        idx = self._url.find(sep)
        if idx == -1:
            return None
        return self._url[:idx]

    def get_host(self) -> str | None:
        sep = "://"
        idx = self._url.find(sep)
        if idx == -1:
            return None
        after_scheme = self._url[idx + len(sep):]
        slash_idx = after_scheme.find("/")
        if slash_idx == -1:
            return after_scheme
        return after_scheme[:slash_idx]

    def get_path(self) -> str | None:
        sep = "://"
        idx = self._url.find(sep)
        if idx == -1:
            return None
        after_scheme = self._url[idx + len(sep):]
        slash_idx = after_scheme.find("/")
        if slash_idx == -1:
            return None
        return after_scheme[slash_idx:]

    def get_query_params(self) -> dict | None:
        q_idx = self._url.find("?")
        if q_idx == -1:
            return None
        fragment_idx = self._url.find("#")
        if fragment_idx != -1 and fragment_idx > q_idx:
            query_string = self._url[q_idx + 1:fragment_idx]
        else:
            query_string = self._url[q_idx + 1:]
        params = {}
        for pair in query_string.split("&"):
            parts = pair.split("=")
            if len(parts) == 2:
                params[parts[0]] = parts[1]
        return params

    def get_fragment(self) -> str | None:
        idx = self._url.find("#")
        if idx == -1:
            return None
        return self._url[idx + 1:]

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
