class CookiesUtil:
    def __init__(self, cookies_file):
        self.cookies_file = cookies_file
        self.cookies = None

    def get_cookies(self, reponse):
        self.cookies = reponse.get('cookies')
        self._save_cookies()
        return self.cookies

    def load_cookies(self):
        try:
            import json
            with open(self.cookies_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except Exception:
            return {}

    def _save_cookies(self):
        try:
            import json
            with open(self.cookies_file, 'w', encoding='utf-8') as f:
                json.dump(self.cookies, f)
            return True
        except Exception:
            return False

    def set_cookies(self, request):
        cookies = self.cookies
        if cookies is None:
            cookies = self.load_cookies()
            self.cookies = cookies

        if isinstance(cookies, dict):
            cookie_str = '; '.join(f'{k}={v}' for k, v in cookies.items())
        else:
            cookie_str = str(cookies)

        request['cookies'] = cookie_str
        return request

import unittest

class CookiesUtilTestLoadCookies(unittest.TestCase):

    def test_load_cookies(self):
        self.cookies_util = CookiesUtil('cookies.json')
        self.assertEqual(self.cookies_util.load_cookies(), {'key1': 'value1', 'key2': 'value2'})

    def test_load_cookies_2(self):
        self.cookies_util = CookiesUtil('cookies.json')
        self.cookies_util.cookies = {'cookies': {'key1': 'value1', 'key2': 'value2'}}
        self.assertEqual(self.cookies_util.load_cookies(), {'key1': 'value1', 'key2': 'value2'})

    def test_load_cookies_3(self):
        self.cookies_util = CookiesUtil('cookies.json')
        self.cookies_util.cookies = {'cookies': {'key1': 'value1', 'key2': 'value2'},
                                     'cookies2': {'key3': 'value3', 'key4': 'value4'}}
        self.assertEqual(self.cookies_util.load_cookies(), {'key1': 'value1', 'key2': 'value2'})

    def test_load_cookies_4(self):
        self.cookies_util = CookiesUtil('cookies.json')
        self.cookies_util.cookies = {'cookies': {'key1': 'value1', 'key2': 'value2'},
                                     'cookies2': {'key3': 'value3', 'key4': 'value4'},
                                     'cookies3': {'key5': 'value5', 'key6': 'value6'}}
        self.assertEqual(self.cookies_util.load_cookies(), {'key1': 'value1', 'key2': 'value2'})

    def test_load_cookies_5(self):
        self.cookies_util = CookiesUtil('cookies.json')
        self.cookies_util.cookies = {'cookies': {'key1': 'value1', 'key2': 'value2'},
                                     'cookies2': {'key3': 'value3', 'key4': 'value4'},
                                     'cookies3': {'key5': 'value5', 'key6': 'value6'},
                                     'cookies4': {'key7': 'value7', 'key8': 'value8'}}
        self.assertEqual(self.cookies_util.load_cookies(), {'key1': 'value1', 'key2': 'value2'})

    def test_load_cookies_6(self):
        self.cookies_util = CookiesUtil('')
        self.assertEqual(self.cookies_util.load_cookies(), {})

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
