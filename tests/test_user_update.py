import allure
import pytest

from src import config
from src.helpers import patch_user


@allure.feature("User")
@allure.story("Update")
class TestUserUpdate:

    @pytest.mark.parametrize(
        "field, value",
        [
            ("name", "NewName"),
            ("email", "new_email_123@example.com"),
            ("password", "new_password_123"),
        ],
    )
    def test_update_user_with_auth_success(self, registered_user, client, field, value):
        _payload, token = registered_user

        resp = patch_user(client, token, {field: value})
        assert resp.status_code == 200

        body = resp.json()
        assert body["success"] is True

        # password обычно не возвращают — проверяем только success
        if field in ("email", "name"):
            assert body["user"][field] == value

    @pytest.mark.parametrize(
        "field, value",
        [
            ("name", "NoAuthName"),
            ("email", "no_auth_email@example.com"),
            ("password", "no_auth_password"),
        ],
    )
    def test_update_user_without_auth_returns_401(self, client, field, value):
        resp = client.request("PATCH", config.USER, json={field: value})
        assert resp.status_code == 401

        body = resp.json()
        assert body["success"] is False
        assert body["message"] == config.ERR_NOT_AUTH
