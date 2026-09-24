class AccessGatewayFilter:
    def __init__(self):
        pass

    def is_start_with(self, path, prefixes=("/api", "/login")):
        if path is None:
            return False
        return any(str(path).startswith(prefix) for prefix in prefixes)

    def filter(self, request):
        try:
            path = request.get("path")
            if self.is_start_with(path):
                return True

            token = self.get_jwt_user(request)
            if not token:
                return False

            user = token.get("user")
            if not isinstance(user, dict):
                return False

            if user.get("level", 0) > 2:
                self.set_current_user_info_and_log(user)
                return True

            return False
        except Exception:
            return False

    def get_jwt_user(self, request):
        import datetime

        headers = request.get("headers", {})
        auth = headers.get("Authorization")
        if not isinstance(auth, dict):
            return None

        user = auth.get("user")
        jwt = auth.get("jwt")
        if not user or not jwt:
            return None

        user_name = user.get("name") if isinstance(user, dict) else None
        if not user_name:
            return None

        jwt = str(jwt)
        user_name = str(user_name)

        if not jwt.startswith(user_name):
            return None

        date_str = jwt[len(user_name):]
        try:
            token_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            return None

        current_date = datetime.date.today()
        if (current_date - token_date).days >= 3:
            return None

        return auth

    def set_current_user_info_and_log(self, user):
        import datetime

        name = user.get("name", "")
        address = user.get("address", "")
        timestamp = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
        message = f"user={name}, address={address}, time={timestamp}"
        print(message)

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
