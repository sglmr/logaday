from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods

from records.forms import RecordSettingForm
from records.models import RecordSetting


@require_http_methods(["GET"])
def home_page_view(request: HttpRequest) -> TemplateResponse:
    if request.user.is_authenticated:
        return redirect("records:edit_today")
    return TemplateResponse(request, "pages/home.html")


@login_required()
@require_http_methods(["GET", "POST"])
def profile_page_view(request: HttpRequest) -> TemplateResponse:
    current_settings = get_object_or_404(RecordSetting, user=request.user)

    if request.method == "POST":
        rs_form = RecordSettingForm(data=request.POST, instance=current_settings)
        if rs_form.is_valid():
            rs_form.save(commit=False)
            rs_form.author = request.user
            rs_form.save()
    if request.method == "GET":
        rs_form = RecordSettingForm(instance=current_settings)

    context = {"record_setting_form": rs_form}
    return TemplateResponse(request, "pages/profile.html", context=context)
