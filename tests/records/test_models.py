import pytest
from records.models import RecordSetting


#      Records List Page Tests
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
