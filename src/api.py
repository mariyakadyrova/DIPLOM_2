from src import config


class ApiClient:
    def __init__(self, client):
        self._client = client

    def request(self, method: str, path: str, **kwargs):
        return self._client.request(method, path, **kwargs)

    @staticmethod
    def auth_headers(access_token: str):
        return {"Authorization": access_token}


class UserApi(ApiClient):
    def register(self, payload):
        return self.request("POST", config.REGISTER, json=payload)

    def login(self, email: str, password: str):
        return self.request("POST", config.LOGIN, json={"email": email, "password": password})

    def patch(self, access_token: str, payload):
        return self.request("PATCH", config.USER, headers=self.auth_headers(access_token), json=payload)

    def delete(self, access_token: str):
        return self.request("DELETE", config.USER, headers=self.auth_headers(access_token))


class IngredientsApi(ApiClient):
    def get(self):
        return self.request("GET", config.INGREDIENTS)


class OrderApi(ApiClient):
    def create(self, ingredient_ids=None, access_token=None):
        headers = {"Authorization": access_token} if access_token else None
        json_body = {"ingredients": ingredient_ids} if ingredient_ids is not None else {}
        return self.request("POST", config.ORDERS, headers=headers, json=json_body)

    def get_user_orders(self, access_token=None):
        headers = {"Authorization": access_token} if access_token else None
        return self.request("GET", config.ORDERS, headers=headers)