import pytest

from records.forms import RecordSettingForm


#   Record Settings Form Tests
# -----------------------------------------------
@pytest.mark.django_db
class TestRecordsSettingForm:
    def test_form_can_be_blank(self, user1):
        form = RecordSettingForm(data={"headings": ""})
        assert len(form.errors) == 0
