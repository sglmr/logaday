import pytest
from records.models import RecordSetting, Record


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
