import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertNotContains, assertTemplateUsed

from records.models import Record


#      Records List Page Tests
# -------------------------------
@pytest.mark.django_db
class TestRecordsListPage:
    @pytest.fixture
    def list_url(self):
        yield reverse("records:list")

    def test_redirect_without_login(self, client, list_url):
        r = client.get(list_url)
        assert r.status_code == 302
        assert r.url == "/accounts/login/?next=/records/list/"

    def test_template_used(self, client, user1, list_url):
        client.force_login(user1)
        r = client.get(list_url)
        assert r.status_code == 200
        assertTemplateUsed(r, "records/list.html")

    def test_list_records_user1_content(self, client, user1, list_url, recs_fixt):
        client.force_login(user1)
        r = client.get(list_url)

        # Make sure there are records
        assert Record.objects.all().count() > 2

        # contains this user's records
        for record in Record.objects.filter(user=user1):
            assertContains(r, record.title)
            assertContains(r, record.content)

        # does not contain other user's records
        for record in Record.objects.all().exclude(user=user1):
            assertNotContains(r, record.title)
            assertNotContains(r, record.content)

    def test_list_records_user2_content(self, client, user2, list_url, recs_fixt):
        client.force_login(user2)
        r = client.get(list_url)

        # contains this user's records
        for record in Record.objects.filter(user=user2):
            assertContains(r, record.title)
            assertContains(r, record.content)

        # does not contain other user's records
        for record in Record.objects.all().exclude(user=user2):
            assertNotContains(r, record.title)
            assertNotContains(r, record.content)


#     Record Edit Page Tests
# -------------------------------
@pytest.mark.django_db
class TestRecordEditPage:
    @pytest.fixture
    def edit_url(self):
        yield reverse("records:edit", kwargs={"date": "2022-01-01"})

    def test_redirect_without_login(self, client, edit_url):
        r = client.get(edit_url)
        assert r.status_code == 302
        assert r.url == "/accounts/login/?next=/records/2022-01-01/"

    def test_template_used(self, client, user1, edit_url):
        client.force_login(user1)
        r = client.get(edit_url)
        assert r.status_code == 200
        assertTemplateUsed(r, "records/workbench.html")
        assertTemplateUsed(r, "records/record_form_partial.html")

    def test_edit_form_contains_correct_content(self, client, user1, recs_fixt):

        r = Record.objects.filter(user=user1).last()
        client.force_login(user1)
        response = client.get(f"/records/{r.date}/")
        assertContains(response, r.title)
        assertContains(response, r.content)

    def test_edit_without_date_creates_todays_record(self, client, user1):
        assert Record.objects.all().count() == 0
        client.force_login(user1)
        client.get("/records/")
        assert Record.objects.all().count() == 1
