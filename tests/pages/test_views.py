import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertContains


#       Home Page Tests
# -------------------------------


@pytest.fixture
@pytest.mark.django_db
def index(client):
    yield client.get(reverse("pages:home"))


@pytest.mark.django_db
def test_home_page_200_status(index):
    assert index.status_code == 200


@pytest.mark.django_db
def test_home_page_location(index):
    assert index.request["PATH_INFO"] == "/"


@pytest.mark.django_db
def test_home_page_template(index):
    assertTemplateUsed(index, "pages/home.html")


@pytest.mark.django_db
def test_home_page_url_contents(index):
    assertContains(index, reverse("account_login"))
    assertContains(index, reverse("account_signup"))


#      Profile Page Tests
# -------------------------------
@pytest.fixture
def profile_page_url():
    yield reverse("pages:profile")


@pytest.mark.django_db
class TestProfilePageWithoutLogin:
    @pytest.fixture
    def profile_page(self, client, profile_page_url):
        yield client.get(profile_page_url)

    def test_status(self, profile_page):
        assert profile_page.status_code == 302

    def test_redirect(self, profile_page):
        assert profile_page.url == "/accounts/login/?next=/profile/"


@pytest.mark.django_db
class TestProfilePage:
    @pytest.fixture
    def profile_page(self, client, user1, profile_page_url):
        client.force_login(user1)
        yield client.get(profile_page_url)

    def test_status(self, profile_page):
        assert profile_page.status_code == 200

    def test_template(self, profile_page):
        assertTemplateUsed(profile_page, "pages/profile.html")

    def test_profile_page_location(self, profile_page):
        assert profile_page.request["PATH_INFO"] == "/profile/"
