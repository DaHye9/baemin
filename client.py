import requests


class Client:
    def __init__(self) -> None:
        self._token = 'test-api-token-12345'
        self._content_type = 'application/json;charset=UTF-8'
        self._base_url = 'https://api-test.fooddelivery.com'

    @property
    def header(self) -> dict[str, str]:
        return {
            'Authorization': f'Bearer {self._token}',
            'Content-Type': self._content_type
        }

    def post(self, route: str, json: dict) -> requests.Response:
        url = f'{self._base_url}{route}'
        return requests.post(url, headers=self.header, json=json)
