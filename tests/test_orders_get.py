import allure
from src import config
from src.helpers import get_ingredients, create_order, get_user_orders


@allure.feature("Orders")
@allure.story("Get user orders")
class TestOrdersGet:

    def test_get_orders_authorized_user_success(self, registered_user, client):
        _payload, token = registered_user

        # Создаём заказ, чтобы гарантировать наличие данных
        ingr = get_ingredients(client).json()
        ingredient_ids = [ingr["data"][0]["_id"], ingr["data"][1]["_id"]]
        create_order(client, ingredient_ids=ingredient_ids, access_token=token)

        resp = get_user_orders(client, access_token=token)
        assert resp.status_code == 200

        body = resp.json()
        assert body["success"] is True
        assert isinstance(body["orders"], list)

    def test_get_orders_unauthorized_returns_401(self, client):
        resp = get_user_orders(client, access_token=None)
        assert resp.status_code == 401

        body = resp.json()
        assert body["success"] is False
        assert body["message"] == config.ERR_NOT_AUTH
