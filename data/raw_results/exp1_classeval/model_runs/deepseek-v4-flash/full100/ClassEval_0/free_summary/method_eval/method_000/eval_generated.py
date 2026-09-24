import base64
import json
import logging
from datetime import datetime, timedelta


class AccessGatewayFilter:
    def __init__(self, user_service=None, logger=None):
        self.user_service = user_service
        self.logger = logger or logging.getLogger(__name__)

    def filter(self, request):
        path = request.get("path", "")

        if self.is_start_with(path):
            return True

        user = self.get_jwt_user(request)
        if not user:
            return False

        if not self.has_permission(user):
            return False

        self.set_current_user_info_and_log(request, user)
        return True

    def is_start_with(self, path):
        return path.startswith("/api") or path.startswith("/login")

    def get_jwt_user(self, request):
        headers = request.get("headers") or {}
        auth_header = headers.get("Authorization") or headers.get("authorization")

        if isinstance(auth_header, list):
            auth_header = auth_header[0] if auth_header else None

        if not auth_header:
            return None

        token = auth_header
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]

        claims = self._decode_jwt(token)
        if not claims:
            return None

        username = claims.get("userName") or claims.get("username") or claims.get("sub")
        if not username:
            return None

        date_value = claims.get("date")
        if date_value is None:
            date_value = claims.get("timestamp")
        if date_value is None:
            date_value = claims.get("iat")
        if date_value is None:
            return None

        token_time = self._parse_date(date_value)
        if token_time is None:
            return None

        if datetime.now() - token_time > timedelta(days=3):
            return None

        return username

    def _decode_jwt(self, token):
        try:
            parts = token.split(".")
            if len(parts) != 3:
                return None

            payload_part = parts[1]
            padding = "=" * (-len(payload_part) % 4)
            decoded = base64.urlsafe_b64decode(
                payload_part.encode("ascii") + padding.encode("ascii")
            )
            return json.loads(decoded.decode("utf-8"))
        except Exception:
            return None

    @staticmethod
    def _parse_date(value):
        if isinstance(value, datetime):
            return value

        if isinstance(value, (int, float)):
            try:
                return datetime.fromtimestamp(value)
            except Exception:
                return None

        if isinstance(value, str):
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue

        return None

    def has_permission(self, username):
        return self._get_access_level(username) > 2

    def _get_access_level(self, username):
        if self.user_service is not None:
            try:
                if callable(self.user_service):
                    return self.user_service(username)
                return self.user_service.get_access_level(username)
            except Exception:
                return 0

        return 3 if username == "admin" else 0

    def set_current_user_info_and_log(self, request, user):
        method = request.get("method", "")
        path = request.get("path", "")
        self.logger.info(
            "user:%s url:%s method:%s time:%s",
            user,
            path,
            method,
            datetime.now(),
        )

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
