import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from records.models import Record, RecordSetting

User = get_user_model()

#    Record Settings Tests
# -------------------------------
@pytest.mark.django_db
class TestRecordsSettingModel:
    def test_record_settings_automatically_created(self, user1):
        assert RecordSetting.objects.filter(user=user1).count() == 1

    def test_record_settings_not_duplicated_created(self, user1):
        user1.save()
        assert RecordSetting.objects.filter(user=user1).count() == 1

    def test_record_settings_default_headings(self, user1):
        assert user1.record_settings.headings == "personal, work"
        assert "# Personal" in user1.record_settings.default_content
        assert "# Work" in user1.record_settings.default_content

    def test_record_settings__str__(self, user1):
        assert f"{user1.record_settings}" == f"{user1} record settings"


#         Record Tests
# -------------------------------
@pytest.mark.django_db
class TestRecordsModel:
    @pytest.fixture
    def _record(self, user1, recs_fixt):
        yield Record.objects.filter(user=user1).last()

    def test_record__str__(self, _record):
        assert f"{_record}" == _record.title

    def test_record_without_titles_title(self, user1):
        # title should be "pretty date" if not supplied
        r = Record.objects.create(
            user=user1, content="blah", date=timezone.now().date()
        )
        assert r.title == r.pretty_date

    def test_content_after_record_creation(self, user1):
        r = Record.objects.create(
            user=user1,
            date=timezone.now().date(),
            title="user1_now_title",
            content="user1_now_content",
        )
        assert r.date == timezone.now().date()
        assert r.user == user1
        assert r.title == "user1_now_title"
        assert r.content == "- user1_now_content"

    def test_default_content_on_record_for_user(self, user1):
        r = Record.objects.create(user=user1, date=timezone.now().date())
        assert r.content == "# Personal\n- \n\n# Work\n- "
