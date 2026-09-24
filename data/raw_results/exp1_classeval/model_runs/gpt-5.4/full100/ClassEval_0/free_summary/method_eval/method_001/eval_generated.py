from datetime import datetime, date


class AccessGatewayFilter:
    def __init__(self):
        self.logs = []

    def filter(self, request):
        path = request["path"]
        method = request["method"]

        if self.is_start_with(path):
            return True

        try:
            token = self.get_jwt_user(request)
            user = token["user"]
            if user["level"] > 2:
                self.set_current_user_info_and_log(user)
                return True
        except Exception:
            return False

    def is_start_with(self, request_uri):
        return request_uri.startswith("/api") or request_uri.startswith("/login")

    def get_jwt_user(self, request):
        token = request["headers"]["Authorization"]
        user = token["user"]
        jwt = token["jwt"]
        name = user["name"]

        if jwt.startswith(name):
            date_str = jwt[len(name):]
            token_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if (date.today() - token_date).days >= 3:
                return None

        return token

    def set_current_user_info_and_log(self, user):
        message = f"{user['name']} {user['address']} {datetime.now().isoformat()}"
        self.logs.append(message)
        return message

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
