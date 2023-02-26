from django.urls import path

from .views import home_page_view, profile_page_view

app_name = "pages"
urlpatterns = [
    path("", home_page_view, name="home"),
    path("profile/", profile_page_view, name="profile"),
]
