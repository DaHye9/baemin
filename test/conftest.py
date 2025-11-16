import pytest

from api.api_client import APIClient


@pytest.fixture(scope='session')
def client() -> APIClient:
    # Intended to be xfail. API doesn't work.
    pytest.xfail()
    return APIClient()