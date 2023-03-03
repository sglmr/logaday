import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertNotContains, assertTemplateUsed

from records.models import Record


#      Records List Page Tests
# -------------------------------
@pytest.mark.django_db
class TestRecordsListPage:
    @pytest.fixture
    def test_url(self):
        yield reverse("records:list")

    def test_redirect_without_login(self, client, test_url):
        r = client.get(test_url)
        assert r.status_code == 302
        assert r.url == "/accounts/login/?next=/records/list/"

    def test_template_used(self, client, user1, test_url):
        client.force_login(user1)
        r = client.get(test_url)
        assert r.status_code == 200
        assertTemplateUsed(r, "records/list.html")

    def test_list_records_user1_content(self, client, user1, test_url, recs_fixt):
        client.force_login(user1)
        r = client.get(test_url)

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

    def test_list_records_user2_content(self, client, user2, test_url, recs_fixt):
        client.force_login(user2)
        r = client.get(test_url)

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
    def test_url(self):
        yield reverse("records:edit", kwargs={"date": "2022-01-01"})

    def test_redirect_without_login(self, client, test_url):
        r = client.get(test_url)
        assert r.status_code == 302
        assert r.url == "/accounts/login/?next=/records/2022-01-01/"

    def test_template_used(self, client, user1, test_url):
        client.force_login(user1)
        r = client.get(test_url)
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


#  Record Form Change View Tests
# -------------------------------------
@pytest.mark.django_db
class TestRecordFormChangeView:
    @pytest.fixture
    def test_url(self):
        yield reverse("records:change_form")

    def test_get_url_redirect_without_login(self, client, test_url):
        r = client.get(test_url)
        assert r.status_code == 302
        assert r.url == "/accounts/login/?next=/records/change_form/"

    def test_get_method_not_allowed(self, client, user1, test_url):
        client.force_login(user1)
        r = client.get(test_url)
        assert r.status_code == 405  # Not Allowed

    def test_empty_post_method_is_not_200(self, client, user1, test_url):
        client.force_login(user1)
        r = client.post(test_url)
        assert r.status_code == 204  # invalid form/post

    def test_template_used(self, client, user1, test_url):
        client.force_login(user1)
        r = client.post(
            test_url,
            data={
                "date": "2022-01-01",
                "title": "Some_Tittle",
                "content": "some_content",
            },
        )
        assert r.status_code == 200
        assertTemplateUsed(r, "records/record_form_partial.html")

    def test_post_can_create_new_record(self, client, user1, test_url):
        assert Record.objects.filter(user=user1, date="1990-01-01").count() == 0
        client.force_login(user1)
        client.post(
            test_url,
            data={
                "date": "1990-01-01",
                "title": "Some_Tittle",
                "content": "some_content",
            },
        )
        assert Record.objects.filter(user=user1, date="1990-01-01").count() == 1

    def test_post_can_return_existing_record(self, client, user1, test_url, recs_fixt):
        assert Record.objects.filter(user=user1, date="1900-02-01").count() == 1
        client.force_login(user1)
        r = client.post(test_url, data={"date": "1900-02-01"})
        assert r.status_code == 200
        assertContains(r, "1900-02-01")
        assertContains(r, "old_user1_post")
        assertContains(r, "user1_old_content")


#  Record Form Save View Tests
# -------------------------------------
@pytest.mark.django_db
class TestRecordFormSaveView:
    @pytest.fixture
    def test_url(self):
        yield reverse("records:save_form")

    def test_get_url_redirect_without_login(self, client, test_url):
        r = client.get(test_url)
        assert r.status_code == 302
        assert r.url == "/accounts/login/?next=/records/save_form/"

    def test_get_method_not_allowed(self, client, user1, test_url):
        client.force_login(user1)
        r = client.get(test_url)
        assert r.status_code == 405  # Not Allowed

    def test_nonexistant_record_404s(self, client, user1, test_url):
        client.force_login(user1)
        r = client.post(test_url, data={"date": "2025-02-02"})
        assert r.status_code == 404

    def test_existing_record_200s(self, client, user1, test_url, recs_fixt):
        client.force_login(user1)
        r = client.post(test_url, data={"date": "1900-02-01"})
        assert r.status_code == 200

    def test_view_saves_record_changes(self, client, user1, test_url, recs_fixt):
        # Establish record starts with expected content
        rec = Record.objects.get(user=user1, date="1900-02-01")
        assert rec.title == "old_user1_post"
        assert rec.content == "- user1_old_content"
        # Post update/save to record with new title and content
        client.force_login(user1)
        r = client.post(
            test_url,
            data={
                "date": "1900-02-01",
                "title": "update_title",
                "content": "update_content1",
            },
        )
        assert r.status_code == 200
        # Check that it changed
        rec = Record.objects.get(user=user1, date="1900-02-01")
        assert rec.title == "update_title"
        assert rec.content == "- update_content1"
