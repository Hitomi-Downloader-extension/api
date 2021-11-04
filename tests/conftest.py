import pytest
from requests import Session


@pytest.fixture
def client():
    session = Session()
    yield session
    session.close()
