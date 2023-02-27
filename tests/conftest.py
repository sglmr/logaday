import pytest
from accounts.models import CustomUser
from logapp.models import Log
from django.utils import timezone


@pytest.fixture
def user1():
    yield CustomUser.objects.create(
        username="example", email="example@example.com", password="SuperSecure123!"
    )


@pytest.fixture
def user2():
    yield CustomUser.objects.create(
        username="example2", email="example2@example.com", password="SuperSecure123!"
    )


@pytest.fixture
def logs_fixt(user1, user2):
    Log.objects.create(
        user=user1,
        date=timezone.now(),
        title="user1_now_title",
        content="user1_now_content",
    )

    Log.objects.create(
        user=user2,
        date=timezone.now(),
        title="user2_now_title",
        content="user2_now_content",
    )
