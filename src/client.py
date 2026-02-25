import allure
import requests


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def request(self, method: str, path: str, headers=None, json=None):
        url = f"{self.base_url}{path}"
        with allure.step(f"{method} {path}"):
            resp = self.session.request(method, url, headers=headers, json=json, timeout=15)
            allure.attach(str(json), "request_json", allure.attachment_type.TEXT)
            allure.attach(f"{resp.status_code}\n{resp.text}", "response", allure.attachment_type.TEXT)
            return resp
