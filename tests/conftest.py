import pytest
from accounts.models import CustomUser


@pytest.fixture
def user1():
    yield CustomUser.objects.create(
        username="example", email="example@example.com", password="SuperSecure123!"
    )


@pytest.fixture
def user1_client(client, user1):
    client.force_login(user1)
    yield client
