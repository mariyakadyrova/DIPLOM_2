from src.api import UserApi, OrderApi, IngredientsApi


def register_user(client, payload):
    return UserApi(client).register(payload)

def login_user(client, email, password):
    return UserApi(client).login(email, password)

def auth_headers(access_token: str):
    return {"Authorization": access_token}

def patch_user(client, access_token: str, payload):
    return UserApi(client).patch(access_token, payload)

def delete_user(client, access_token: str):
    return UserApi(client).delete(access_token)

def get_ingredients(client):
    return IngredientsApi(client).get()

def create_order(client, ingredient_ids=None, access_token=None):
    return OrderApi(client).create(ingredient_ids=ingredient_ids, access_token=access_token)

def get_user_orders(client, access_token=None):
    return OrderApi(client).get_user_orders(access_token=access_token)
