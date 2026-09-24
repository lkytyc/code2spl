import datetime
import logging


class AccessGatewayFilter:
    def __init__(self):
        pass

    def filter(self, request):
        try:
            request_uri = request['path']
            method = request['method']
            if self.is_start_with(request_uri):
                return True
            token = self.get_jwt_user(request)
            user = token['user']
            if user['level'] > 2:
                self.set_current_user_info_and_log(user)
                return True
        except Exception:
            return False
        return False

    def is_start_with(self, request_uri):
        start_with = ['/api', '/login']
        for s in start_with:
            if request_uri.startswith(s):
                return True
        return False

    def get_jwt_user(self, request):
        token = request['headers']['Authorization']
        user = token['user']
        jwt_prefix_matches_user_name = token['jwt'].startswith(user['name'])
        if jwt_prefix_matches_user_name:
            jwt_str_date = token['jwt'].split(user['name'])[1]
            jwt_date = datetime.datetime.strptime(jwt_str_date, "%Y-%m-%d")
            is_jwt_at_least_3_days_old = datetime.datetime.today() - jwt_date >= datetime.timedelta(days=3)
            if is_jwt_at_least_3_days_old:
                return None
        return token

    def set_current_user_info_and_log(self, user):
        host = user['address']
        logging.log(1, f"{user['name']} {host} {datetime.datetime.now()}")

import unittest

class AccessGatewayFilterTest(unittest.TestCase):
    def test_AccessGatewayFilter(self):
        agf = AccessGatewayFilter()
        request = {'path': '/api/data', 'method': 'GET'}
        res = agf.filter(request)
        self.assertTrue(res)

        request_uri = '/api/data'
        res = agf.is_start_with(request_uri)
        self.assertTrue(res)

        request = {
            'headers': {'Authorization': {'user': {'name': 'user1'}, 'jwt': 'user1' + str(datetime.date.today())}}}
        res = agf.get_jwt_user(request)
        self.assertIsNotNone(res)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
