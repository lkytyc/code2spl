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
