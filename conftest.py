import pytest
from src.client import ApiClient
from src import config
from src.data import random_user_payload
from src.helpers import register_user, delete_user

@pytest.fixture()
def client():
    return ApiClient(config.BASE_URL)

@pytest.fixture()
def registered_user(client):
    payload = random_user_payload()
    resp = register_user(client, payload)
    assert resp.status_code == 200
    body = resp.json()
    access_token = body["accessToken"]

    yield payload, access_token

    delete_user(client, access_token)
