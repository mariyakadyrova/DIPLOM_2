import allure
from src import config
from src.helpers import get_ingredients, create_order


@allure.feature("Orders")
@allure.story("Create")
class TestOrdersCreate:

    def test_create_order_with_auth_and_ingredients_success(self, registered_user, client):
        _payload, token = registered_user

        ingr_resp = get_ingredients(client)
        assert ingr_resp.status_code == 200
        ingr = ingr_resp.json()
        ingredient_ids = [ingr["data"][0]["_id"], ingr["data"][1]["_id"]]

        resp = create_order(client, ingredient_ids=ingredient_ids, access_token=token)
        assert resp.status_code == 200

        body = resp.json()
        assert body["success"] is True
        assert "order" in body and "number" in body["order"]

    def test_create_order_without_auth_success(self, client):
        ingr_resp = get_ingredients(client)
        assert ingr_resp.status_code == 200
        ingr = ingr_resp.json()
        ingredient_ids = [ingr["data"][0]["_id"]]

        resp = create_order(client, ingredient_ids=ingredient_ids, access_token=None)
        assert resp.status_code == 200

        body = resp.json()
        assert body["success"] is True
        assert "order" in body and "number" in body["order"]

    def test_create_order_without_ingredients_returns_400(self, registered_user, client):
        _payload, token = registered_user

        resp = create_order(client, ingredient_ids=[], access_token=token)
        assert resp.status_code == 400

        body = resp.json()
        assert body["success"] is False
        assert body["message"] == config.ERR_NO_INGREDIENTS

    def test_create_order_with_invalid_ingredient_hash_returns_400(self, registered_user, client):
        _payload, token = registered_user

        resp = create_order(client, ingredient_ids=["invalid_hash"], access_token=token)
        assert resp.status_code == 400

        body = resp.json()
        assert body["success"] is False
        assert "message" in body
