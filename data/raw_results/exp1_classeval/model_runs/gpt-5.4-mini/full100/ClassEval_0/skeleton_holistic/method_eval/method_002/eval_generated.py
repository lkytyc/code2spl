import logging
import datetime

class AccessGatewayFilter:
    """
    This class is a filter used for accessing gateway filtering, primarily for authentication and access log recording.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.current_user = None

    def filter(self, request):
        """
        Filter the incoming request based on certain rules and conditions.
        :param request: dict, the incoming request details
        :return: bool, True if the request is allowed, False otherwise
        >>> filter = AccessGatewayFilter()
        >>> filter.filter({'path': '/login', 'method': 'POST'})
        True

        """
        if not isinstance(request, dict):
            return False

        path = request.get('path', '')
        if self.is_start_with(path):
            user = self.get_jwt_user(request)
            if user is not None:
                self.set_current_user_info_and_log(user)
                return True
            return False

        return True

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
        if not isinstance(request_uri, str):
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
        if not isinstance(request, dict):
            return None

        headers = request.get('headers', {})
        auth = headers.get('Authorization')
        if not isinstance(auth, dict):
            return None

        user = auth.get('user')
        jwt = auth.get('jwt')
        if user is None or jwt is None:
            return None

        expected_jwt = str(user.get('name', '')) + str(datetime.date.today())
        if jwt == expected_jwt:
            return {'user': user}
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
        self.current_user = user
        self.logger.info("Access granted for user: %s", user)

import unittest

class AccessGatewayFilterTestGetJwtUser(unittest.TestCase):
    def test_get_jwt_user_1(self):
        agf = AccessGatewayFilter()
        request = {
            'headers': {'Authorization': {'user': {'name': 'user1'}, 'jwt': 'user1' + str(datetime.date.today())}}}
        res = agf.get_jwt_user(request)
        self.assertIsNotNone(res)

    def test_get_jwt_user_2(self):
        agf = AccessGatewayFilter()
        request = {
            'headers': {'Authorization': {'user': {'name': 'user2'}, 'jwt': 'user2' + str(datetime.date.today())}}}
        res = agf.get_jwt_user(request)
        self.assertIsNotNone(res)

    def test_get_jwt_user_3(self):
        agf = AccessGatewayFilter()
        request = {
            'headers': {'Authorization': {'user': {'name': 'user3'}, 'jwt': 'user3' + str(datetime.date.today())}}}
        res = agf.get_jwt_user(request)
        self.assertIsNotNone(res)

    def test_get_jwt_user_4(self):
        agf = AccessGatewayFilter()
        request = {
            'headers': {'Authorization': {'user': {'name': 'user4'}, 'jwt': 'user4' + str(datetime.date.today())}}}
        res = agf.get_jwt_user(request)
        self.assertIsNotNone(res)

    def test_get_jwt_user_5(self):
        agf = AccessGatewayFilter()
        request = {'headers': {'Authorization': {'user': {'name': 'user1'}, 'jwt': 'user1' + str(
            datetime.date.today() - datetime.timedelta(days=5))}}}
        res = agf.get_jwt_user(request)
        self.assertIsNone(res)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
