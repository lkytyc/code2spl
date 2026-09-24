class URLHandler:
    def __init__(self, url: str):
        self.url = url

    def get_fragment(self) -> str | None:
        fragment_start = self.url.find('#')
        has_fragment = fragment_start != -1
        if has_fragment:
            return self.url[fragment_start + 1:]
        return None

    def get_host(self) -> str | None:
        scheme_end = self.url.find('://')
        scheme_present = scheme_end != -1
        if scheme_present:
            url_without_scheme = self.url[scheme_end + 3:]
            host_end = url_without_scheme.find('/')
            path_present = host_end != -1
            if path_present:
                return url_without_scheme[:host_end]
            return url_without_scheme
        return None

    def get_path(self) -> str | None:
        scheme_end = self.url.find('://')
        outer_condition_passed = scheme_end != -1
        if outer_condition_passed:
            url_without_scheme = self.url[scheme_end + 3:]
            host_end = url_without_scheme.find('/')
            inner_condition_passed = host_end != -1
            if inner_condition_passed:
                return url_without_scheme[host_end:]
        return None

    def get_query_params(self) -> dict | None:
        query_start = self.url.find('?')
        fragment_start = self.url.find('#')
        condition_query_exists = query_start != -1
        if condition_query_exists:
            if fragment_start == -1:
                query_string = self.url[query_start + 1:]
            else:
                query_string = self.url[query_start + 1:fragment_start]
            params = {}
            condition_query_nonempty = len(query_string) > 0
            if condition_query_nonempty:
                param_pairs = query_string.split('&')
                for segment in param_pairs:
                    key_value = segment.split('=')
                    condition_well_formed_pair = len(key_value) == 2
                    if condition_well_formed_pair:
                        key, value = key_value
                        params[key] = value
            return params
        return None

    def get_scheme(self) -> str | None:
        scheme_end = self.url.find('://')
        found_delimiter = scheme_end != -1
        if found_delimiter:
            return self.url[:scheme_end]
        return None

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
