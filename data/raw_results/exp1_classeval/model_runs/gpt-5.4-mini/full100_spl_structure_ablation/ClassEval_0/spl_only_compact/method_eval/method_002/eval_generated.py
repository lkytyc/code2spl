import datetime
import logging


class AccessGatewayFilter:
    def __init__(self):
        pass

    def filter(self, request: dict) -> bool:
        request_uri = request["path"]
        method = request["method"]
        if self.is_start_with(request_uri):
            return True
        try:
            token = self.get_jwt_user(request)
            if token is None:
                return False
            user = token["user"]
            if user["level"] > 2:
                self.set_current_user_info_and_log(user)
                return True
            return False
        except Exception:
            return False

    def get_jwt_user(self, request: dict):
        token = request["headers"]["Authorization"]
        user = token["user"]
        jwt_prefix_matches_user_name = token["jwt"].startswith(user["name"])
        if jwt_prefix_matches_user_name:
            jwt_str_date = token["jwt"].split(user["name"])[1]
            jwt_date = datetime.datetime.strptime(jwt_str_date, "%Y-%m-%d")
            is_jwt_at_least_3_days_old = (
                datetime.datetime.today() - jwt_date >= datetime.timedelta(days=3)
            )
            if is_jwt_at_least_3_days_old:
                return None
        return token

    def is_start_with(self, request_uri: str) -> bool:
        start_with = ["/api", "/login"]
        for s in start_with:
            if request_uri.startswith(s):
                return True
        return False

    def set_current_user_info_and_log(self, user: dict):
        host = user["address"]
        logging.log(1, f"{user['name']} {host} {str(datetime.datetime.now())}")

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
