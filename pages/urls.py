from django.urls import path

from .views import HomePageView, ProfilePageView

app_name = "pages"
urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("profile/", ProfilePageView.as_view(), name="profile"),
]
