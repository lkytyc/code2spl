import json
import os


class CookiesUtil:
    def __init__(self, file_path):
        self.file_path = file_path
        self.cookies = None

    def get_cookies(self, reponse):
        self.cookies = reponse['cookies']
        self._save_cookies()

    def load_cookies(self):
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def _save_cookies(self):
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.cookies, f)
            return True
        except:
            return False

    def set_cookies(self, request):
        request['cookies'] = '; '.join(
            f'{key}={value}' for key, value in self.cookies.items()
        )

import unittest

class CookiesUtilTestGetCookies(unittest.TestCase):

    def test_get_cookies(self):
        self.cookies_util = CookiesUtil('cookies.json')
        self.response = {'cookies': {'key1': 'value1', 'key2': 'value2'}}
        self.cookies_util.get_cookies(self.response)
        self.assertEqual(self.cookies_util.cookies, {'key1': 'value1', 'key2': 'value2'})

    def test_get_cookies_2(self):
        self.cookies_util = CookiesUtil('cookies.json')
        self.response = {'cookies': {'key1': 'value1', 'key2': 'value2'},
                         'cookies2': {'key3': 'value3', 'key4': 'value4'}}
        self.cookies_util.get_cookies(self.response)
        self.assertEqual(self.cookies_util.cookies, {'key1': 'value1', 'key2': 'value2'})

    def test_get_cookies_3(self):
        self.cookies_util = CookiesUtil('cookies.json')
        self.response = {'cookies': {'key1': 'value1', 'key2': 'value2'},
                         'cookies2': {'key3': 'value3', 'key4': 'value4'},
                         'cookies3': {'key5': 'value5', 'key6': 'value6'}}
        self.cookies_util.get_cookies(self.response)
        self.assertEqual(self.cookies_util.cookies, {'key1': 'value1', 'key2': 'value2'})

    def test_get_cookies_4(self):
        self.cookies_util = CookiesUtil('cookies.json')
        self.response = {'cookies': {'key1': 'value1', 'key2': 'value2'},
                         'cookies2': {'key3': 'value3', 'key4': 'value4'},
                         'cookies3': {'key5': 'value5', 'key6': 'value6'},
                         'cookies4': {'key7': 'value7', 'key8': 'value8'}}
        self.cookies_util.get_cookies(self.response)
        self.assertEqual(self.cookies_util.cookies, {'key1': 'value1', 'key2': 'value2'})

    def test_get_cookies_5(self):
        self.cookies_util = CookiesUtil('cookies.json')
        self.response = {'cookies': {'key1': 'value1', 'key2': 'value2'},
                         'cookies2': {'key3': 'value3', 'key4': 'value4'},
                         'cookies3': {'key5': 'value5', 'key6': 'value6'},
                         'cookies4': {'key7': 'value7', 'key8': 'value8'},
                         'cookies5': {'key9': 'value9', 'key10': 'value10'}}
        self.cookies_util.get_cookies(self.response)
        self.assertEqual(self.cookies_util.cookies, {'key1': 'value1', 'key2': 'value2'})

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
