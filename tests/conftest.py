import pytest
from django.contrib.auth import get_user_model
from records.models import Record
from django.utils import timezone

User = get_user_model()


@pytest.fixture
def user1():
    yield User.objects.create(email="example@example.com", password="SuperSecure123!")


@pytest.fixture
def user2():
    yield User.objects.create(email="example2@example.com", password="SuperSecure123!")


@pytest.fixture
def recs_fixt(user1, user2):
    Record.objects.create(
        user=user1,
        date=timezone.now(),
        title="user1_now_title",
        content="user1_now_content",
    )

    Record.objects.create(
        user=user1,
        date="1900-02-01",
        title="old_user1_post",
        content="user1_old_content",
    )

    Record.objects.create(
        user=user2,
        date=timezone.now(),
        title="user2_now_title",
        content="user2_now_content",
    )
    Record.objects.create(
        user=user2,
        date="1900-02-01",
        title="old_user2_post",
        content="user2_old_content",
    )
