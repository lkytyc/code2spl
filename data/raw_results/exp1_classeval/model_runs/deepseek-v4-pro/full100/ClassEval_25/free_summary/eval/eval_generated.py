class CookiesUtil:
    def __init__(self, file_path):
        self.file_path = file_path
        self.cookies = None

    def get_cookies(self, response):
        self.cookies = response.get('cookies')
        self._save_cookies()

    def load_cookies(self):
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_cookies(self):
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.cookies, f)
            return True
        except Exception:
            return False

    def set_cookies(self, request):
        if self.cookies:
            request['cookies'] = '; '.join(f"{k}={v}" for k, v in self.cookies.items())
        else:
            request['cookies'] = ''

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


class CookiesUtilTestSaveCookies(unittest.TestCase):
    def setUp(self):
        self.cookies_util = CookiesUtil('cookies.json')
        self.cookies_util.cookies = {'cookies': {'key1': 'value1', 'key2': 'value2'}}

    def test_save_cookies(self):
        self.assertTrue(self.cookies_util._save_cookies())

    def test_save_cookies_2(self):
        self.cookies_util.cookies = {'cookies': {'key1': 'value1', 'key2': 'value2'},
                                     'cookies2': {'key3': 'value3', 'key4': 'value4'}}
        self.assertTrue(self.cookies_util._save_cookies())

    def test_save_cookies_3(self):
        self.cookies_util.cookies = {'cookies': {'key1': 'value1', 'key2': 'value2'},
                                     'cookies2': {'key3': 'value3', 'key4': 'value4'},
                                     'cookies3': {'key5': 'value5', 'key6': 'value6'}}
        self.assertTrue(self.cookies_util._save_cookies())

    def test_save_cookies_4(self):
        self.cookies_util.cookies = {'cookies': {'key1': 'value1', 'key2': 'value2'},
                                     'cookies2': {'key3': 'value3', 'key4': 'value4'},
                                     'cookies3': {'key5': 'value5', 'key6': 'value6'},
                                     'cookies4': {'key7': 'value7', 'key8': 'value8'}}
        self.assertTrue(self.cookies_util._save_cookies())

    def test_save_cookies_5(self):
        self.cookies_util.cookies = {'cookies': {'key1': 'value1', 'key2': 'value2'},
                                     'cookies2': {'key3': 'value3', 'key4': 'value4'},
                                     'cookies3': {'key5': 'value5', 'key6': 'value6'},
                                     'cookies4': {'key7': 'value7', 'key8': 'value8'},
                                     'cookies5': {'key9': 'value9', 'key10': 'value10'}}
        self.assertTrue(self.cookies_util._save_cookies())

    def test_save_cookies_6(self):
        self.cookies_util = CookiesUtil('')
        self.assertFalse(self.cookies_util._save_cookies())


class CookiesUtilTestSetCookies(unittest.TestCase):
    def setUp(self):
        self.cookies_util = CookiesUtil('cookies.json')
        self.cookies_util.cookies = {'cookies': {'key1': 'value1', 'key2': 'value2'}}

    def test_set_cookies(self):
        request = {}
        self.cookies_util.set_cookies(request)
        self.assertEqual(request['cookies'], "cookies={'key1': 'value1', 'key2': 'value2'}")


class CookiesUtilTestMain(unittest.TestCase):
    def setUp(self):
        self.cookies_util = CookiesUtil('cookies.json')
        self.cookies_data = {'cookies': {'key1': 'value1', 'key2': 'value2'}}

    def test_main(self):
        self.cookies_util.get_cookies(self.cookies_data)
        self.assertEqual(self.cookies_util.cookies, {'key1': 'value1', 'key2': 'value2'})
        self.assertEqual(self.cookies_util.load_cookies(), {'key1': 'value1', 'key2': 'value2'})
        self.assertTrue(self.cookies_util._save_cookies())

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
