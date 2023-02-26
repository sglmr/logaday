import pytest


@pytest.mark.django_db
class TestCustomUserModel:
    def test_new_user_fields(self, user1):
        assert user1.username == "example"
        assert user1.email == "example@example.com"

    @pytest.mark.django_db
    def test_new_user___str__(self, user1):
        assert f"{user1}" == user1.email

    @pytest.mark.django_db
    def test_new_user_log_sections(self, user1):
        assert user1.log_sections == "personal, work"

    @pytest.mark.django_db
    def test_new_user_default_log_content(self, user1):
        assert "# Personal" in user1.default_log_content
        assert "# Work" in user1.default_log_content
