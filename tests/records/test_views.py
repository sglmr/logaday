import pytest
from records.models import Record
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertContains, assertNotContains


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
