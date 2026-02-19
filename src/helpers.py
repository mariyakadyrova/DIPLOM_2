from src import config

def register_user(client, payload):
    return client.request("POST", config.REGISTER, json=payload)

def login_user(client, email, password):
    return client.request("POST", config.LOGIN, json={"email": email, "password": password})

def auth_headers(access_token: str):
    return {"Authorization": access_token}

def patch_user(client, access_token: str, payload):
    return client.request("PATCH", config.USER, headers=auth_headers(access_token), json=payload)

def delete_user(client, access_token: str):
    return client.request("DELETE", config.USER, headers=auth_headers(access_token))

def get_ingredients(client):
    return client.request("GET", config.INGREDIENTS)

def create_order(client, ingredient_ids=None, access_token=None):
    headers = {"Authorization": access_token} if access_token else None
    json_body = {"ingredients": ingredient_ids} if ingredient_ids is not None else {}
    return client.request("POST", config.ORDERS, headers=headers, json=json_body)

def get_user_orders(client, access_token=None):
    headers = {"Authorization": access_token} if access_token else None
    return client.request("GET", config.ORDERS, headers=headers)
