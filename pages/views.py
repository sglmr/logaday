from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class ProfilePageView(TemplateView):
    template_name = "pages/profile.html"
