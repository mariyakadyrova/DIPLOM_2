import random
import string

def random_email():
    suffix = "".join(random.choice(string.ascii_lowercase) for _ in range(10))
    return f"test_{suffix}@example.com"

def random_user_payload():
    return {"email": random_email(), "password": "password123", "name": "Username"}
