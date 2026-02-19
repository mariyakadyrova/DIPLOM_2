import allure
import pytest

from src import config
from src.data import random_user_payload
from src.helpers import register_user, delete_user


@allure.feature("User")
@allure.story("Register")
class TestUserRegister:

    def test_create_unique_user(self, client):
        payload = random_user_payload()

        resp = register_user(client, payload)
        assert resp.status_code == 200

        body = resp.json()
        assert body["success"] is True
        assert body["user"]["email"] == payload["email"]
        assert body["user"]["name"] == payload["name"]
        assert "accessToken" in body
        assert "refreshToken" in body

        delete_user(client, body["accessToken"])

    def test_create_existing_user_returns_403(self, client):
        payload = random_user_payload()

        r1 = register_user(client, payload)
        assert r1.status_code == 200
        token = r1.json()["accessToken"]

        r2 = register_user(client, payload)
        assert r2.status_code == 403
        body2 = r2.json()
        assert body2["success"] is False
        assert body2["message"] == config.ERR_USER_EXISTS

        delete_user(client, token)

    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_required_field_returns_403(self, client, missing_field):
        payload = random_user_payload()
        payload.pop(missing_field)

        resp = register_user(client, payload)
        assert resp.status_code == 403
        body = resp.json()
        assert body["success"] is False
        assert body["message"] == config.ERR_REQUIRED_FIELDS
