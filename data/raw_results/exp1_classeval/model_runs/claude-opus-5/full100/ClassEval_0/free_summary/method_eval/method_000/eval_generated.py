import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class AccessGatewayFilter:

    OPEN_ROUTE_PREFIXES = ('/api', '/login')

    def filter(self, request):
        path = request.get('path', '')
        # method is extracted but never used (documented behavior)
        method = request.get('method', '')

        if any(path.startswith(prefix) for prefix in self.OPEN_ROUTE_PREFIXES):
            return True

        try:
            token = self.get_jwt_user(request)
            user = token['user']
            if user['level'] > 2:
                self.set_current_user_info_and_log(user)
                return True
            return False
        except Exception:
            return False

    def get_jwt_user(self, request):
        headers = request.get('headers', {})
        auth_header = headers.get('Authorization', '')
        token_str = auth_header

        # token dict is expected to have at least 'user' and 'jwt' keys
        # Parse the token — expects a dict-like structure encoded in the header.
        # Concrete parsing depends on the upstream token format; here we expect
        # the Authorization header to carry a dict with 'jwt' and 'user' fields.
        import json
        token = json.loads(token_str)

        jwt_string = token.get('jwt', '')
        user_name = token.get('user', {}).get('name', '')

        if jwt_string.startswith(user_name):
            # Strip the username prefix and parse the remainder as a date
            date_str = jwt_string[len(user_name):]
            token_date = datetime.strptime(date_str, '%Y-%m-%d')
            if datetime.utcnow() - token_date >= timedelta(days=3):
                return None

        return token

    def set_current_user_info_and_log(self, user):
        name = user.get('name', '')
        address = user.get('address', '')
        timestamp = datetime.utcnow().isoformat()
        logger.log(1, 'user=%s address=%s time=%s', name, address, timestamp)

import unittest

class AccessGatewayFilterTestFilter(unittest.TestCase):
    def test_filter_1(self):
        agf = AccessGatewayFilter()
        request = {'path': '/api/data', 'method': 'GET'}
        res = agf.filter(request)
        self.assertTrue(res)

    def test_filter_2(self):
        agf = AccessGatewayFilter()
        request = {'path': '/api/data', 'method': 'POST'}
        res = agf.filter(request)
        self.assertTrue(res)

    def test_filter_3(self):
        agf = AccessGatewayFilter()
        request = {'path': '/login/data', 'method': 'GET'}
        res = agf.filter(request)
        self.assertTrue(res)

    def test_filter_4(self):
        agf = AccessGatewayFilter()
        request = {'path': '/login/data', 'method': 'POST'}
        res = agf.filter(request)
        self.assertTrue(res)

    def test_filter_5(self):
        agf = AccessGatewayFilter()
        request = {'path': '/abc', 'method': 'POST',
                   'headers': {
                       'Authorization': {'user': {'name': 'user1', 'level': 5, 'address': 'address1'},
                                         'jwt': 'user1' + str(datetime.date.today())}}}
        res = agf.filter(request)
        self.assertTrue(res)

    def test_filter_6(self):
        agf = AccessGatewayFilter()
        request = {'path': '/abc', 'method': 'POST',
                   'headers': {
                       'Authorization': {'user': {'name': 'user1', 'level': 3, 'address': 'address1'},
                                         'jwt': 'user1' + str(datetime.date.today() - datetime.timedelta(days=365))}}}
        res = agf.filter(request)
        self.assertFalse(res)

    def test_filter_7(self):
        agf = AccessGatewayFilter()
        request = {'path': '/abc', 'method': 'POST',
                   'headers': {
                       'Authorization': {'user': {'name': 'user1', 'level': 1, 'address': 'address1'},
                                         'jwt': 'user1' + str(datetime.date.today())}}}
        res = agf.filter(request)
        self.assertIsNone(res)

    def test_filter_8(self):
        agf = AccessGatewayFilter()
        request = {'path': '/abc', 'method': 'POST',
                   'headers': {
                       'Authorization': {'user': {'name': 'user1', 'level': 3, 'address': 'address1'},
                                         'jwt': 'user2' + str(datetime.date.today() - datetime.timedelta(days=365))}}}
        res = agf.filter(request)
        self.assertTrue(res)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
