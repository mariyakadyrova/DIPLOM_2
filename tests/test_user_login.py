import allure
from src import config
from src.helpers import login_user


@allure.feature("User")
@allure.story("Login")
class TestUserLogin:

    def test_login_existing_user_success(self, registered_user, client):
        payload, _token = registered_user

        resp = login_user(client, payload["email"], payload["password"])
        assert resp.status_code == 200

        body = resp.json()
        assert body["success"] is True
        assert "accessToken" in body
        assert "refreshToken" in body
        assert body["user"]["email"] == payload["email"]
        assert body["user"]["name"] == payload["name"]

    def test_login_with_wrong_credentials_returns_401(self, client):
        resp = login_user(client, "wrong_email@example.com", "wrong_password")
        assert resp.status_code == 401

        body = resp.json()
        assert body["success"] is False
        assert body["message"] == config.ERR_LOGIN_INCORRECT
