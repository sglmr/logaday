import pytest
from django.conf import settings
from accounts.models import CustomUser


@pytest.fixture
@pytest.mark.django_db
def user1():
    yield CustomUser.objects.create(
        username="example", email="example@example.com", password="SuperSecure123!"
    )


@pytest.mark.django_db
def test_new_user_fields(user1):
    assert user1.username == "example"
    assert user1.email == "example@example.com"
