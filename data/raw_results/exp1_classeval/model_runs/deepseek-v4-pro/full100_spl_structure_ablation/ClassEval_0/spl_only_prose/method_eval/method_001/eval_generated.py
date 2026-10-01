import datetime
import logging


class AccessGatewayFilter:
    def __init__(self):
        pass

    def filter(self, request):
        request_uri = request['path']
        method = request['method']
        if self.is_start_with(request_uri):
            return True
        try:
            token = self.get_jwt_user(request)
            user = token['user']
            if user['level'] > 2:
                self.set_current_user_info_and_log(user)
                return True
        except Exception:
            return False

    def get_jwt_user(self, request):
        token = request['headers']['Authorization']
        user = token['user']
        if token['jwt'].startswith(user['name']):
            jwt_str_date = token['jwt'].split(user['name'])[1]
            jwt_date = datetime.datetime.strptime(jwt_str_date, '%Y-%m-%d')
            if (datetime.datetime.now() - jwt_date).days >= 3:
                return None
        return token

    def is_start_with(self, request_uri):
        start_with = ["/api", "/login"]
        for s in start_with:
            if request_uri.startswith(s):
                return True
        return False

    def set_current_user_info_and_log(self, user):
        host = user['address']
        message = user['name'] + host + str(datetime.datetime.now())
        logging.log(1, message)

import unittest

class AccessGatewayFilterTestIsStartWith(unittest.TestCase):
    def test_is_start_with_1(self):
        agf = AccessGatewayFilter()
        request_uri = '/api/data'
        res = agf.is_start_with(request_uri)
        self.assertTrue(res)

    def test_is_start_with_2(self):
        agf = AccessGatewayFilter()
        request_uri = '/admin/settings'
        res = agf.is_start_with(request_uri)
        self.assertFalse(res)

    def test_is_start_with_3(self):
        agf = AccessGatewayFilter()
        request_uri = '/login/data'
        res = agf.is_start_with(request_uri)
        self.assertTrue(res)

    def test_is_start_with_4(self):
        agf = AccessGatewayFilter()
        request_uri = '/abc/data'
        res = agf.is_start_with(request_uri)
        self.assertFalse(res)

    def test_is_start_with_5(self):
        agf = AccessGatewayFilter()
        request_uri = '/def/data'
        res = agf.is_start_with(request_uri)
        self.assertFalse(res)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
