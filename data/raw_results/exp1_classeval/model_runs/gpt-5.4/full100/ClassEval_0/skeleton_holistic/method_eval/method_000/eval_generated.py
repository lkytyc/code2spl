import logging
import datetime

class AccessGatewayFilter:
    """
    This class is a filter used for accessing gateway filtering, primarily for authentication and access log recording.
    """

    def __init__(self):
        pass

    def filter(self, request):
        """
        Filter the incoming request based on certain rules and conditions.
        :param request: dict, the incoming request details
        :return: bool, True if the request is allowed, False otherwise
        >>> filter = AccessGatewayFilter()
        >>> filter.filter({'path': '/login', 'method': 'POST'})
        True

        """
        request = request or {}
        path = request.get('path', '')
        if self.is_start_with(path):
            if path.startswith('/api'):
                user = self.get_jwt_user(request)
                if user is None:
                    return False
                self.set_current_user_info_and_log(user)
            return True
        return False

    def is_start_with(self, request_uri):
        """
        Check if the request URI starts with certain prefixes.
        Currently, the prefixes being checked are "/api" and "/login".
        :param request_uri: str, the URI of the request
        :return: bool, True if the URI starts with certain prefixes, False otherwise
        >>> filter = AccessGatewayFilter()
        >>> filter.is_start_with('/api/data')
        True

        """
        if not request_uri:
            return False
        return request_uri.startswith('/api') or request_uri.startswith('/login')

    def get_jwt_user(self, request):
        """
        Get the user information from the JWT token in the request.
        :param request: dict, the incoming request details
        :return: dict or None, the user information if the token is valid, None otherwise
        >>> filter = AccessGatewayFilter()
        >>> filter.get_jwt_user({'headers': {'Authorization': {'user': {'name': 'user1'}, 'jwt': 'user1'+str(datetime.date.today())}}})
        {'user': {'name': 'user1'}

        """
        try:
            headers = (request or {}).get('headers', {})
            auth = headers.get('Authorization')
            if not isinstance(auth, dict):
                return None
            token = auth.get('jwt')
            user = auth.get('user')
            if not token or not isinstance(user, dict):
                return None
            username = user.get('name', '')
            expected = f"{username}{datetime.date.today()}"
            if token == expected:
                return {'user': user}
            return None
        except Exception:
            logging.exception("Failed to get JWT user")
            return None

    def set_current_user_info_and_log(self, user):
        """
        Set the current user information and log the access.
        :param user: dict, the user information
        :return: None
        >>> filter = AccessGatewayFilter()
        >>> user = {'name': 'user1', 'address': '127.0.0.1'}
        >>> filter.set_current_user_info_and_log(user)

        """
        try:
            logging.info("Access by user: %s", user)
        except Exception:
            logging.exception("Failed to log user access")

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
