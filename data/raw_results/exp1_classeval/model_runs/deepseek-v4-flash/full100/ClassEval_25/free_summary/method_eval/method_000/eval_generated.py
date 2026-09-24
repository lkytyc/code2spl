import json

class CookiesUtil:
    def __init__(self, file_path):
        self.file_path = file_path
        self.cookies = {}

    def get_cookies(self, response):
        if isinstance(response, dict):
            cookie_data = response.get('cookies', {})
            extracted = self._extract_cookies(cookie_data)
            self.cookies.update(extracted)
            self._save_cookies()
        return self.cookies

    def load_cookies(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            if not isinstance(cookies, dict):
                cookies = {}
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            cookies = {}
        self.cookies = cookies
        return self.cookies

    def _save_cookies(self):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.cookies, f)
            return True
        except (OSError, TypeError):
            return False

    def set_cookies(self, request):
        if isinstance(request, dict):
            request['cookies'] = '; '.join(
                f'{key}={value}' for key, value in self.cookies.items()
            )

    def _extract_cookies(self, cookie_data):
        cookies = {}
        if isinstance(cookie_data, dict):
            if 'name' in cookie_data and 'value' in cookie_data:
                cookies[cookie_data['name']] = cookie_data['value']
            else:
                for key, value in cookie_data.items():
                    if isinstance(value, dict) and 'value' in value:
                        cookies[key] = value['value']
                    else:
                        cookies[key] = value
        else:
            try:
                for item in cookie_data:
                    if isinstance(item, dict):
                        if 'name' in item and 'value' in item:
                            cookies[item['name']] = item['value']
                        else:
                            for k, v in item.items():
                                cookies[k] = v
                    elif hasattr(item, 'name') and hasattr(item, 'value'):
                        cookies[item.name] = item.value
            except TypeError:
                pass
        return cookies

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
