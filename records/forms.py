from django.forms import ModelForm
from django.forms.widgets import DateInput, Textarea, TextInput
from django.urls import reverse_lazy

from .models import Record, RecordSetting


class RecordSettingForm(ModelForm):
    class Meta:
        model = RecordSetting
        fields = ["headings"]
        help_texts = {"headings": "(Default headings for new records)"}

        widgets = {
            "headings": TextInput(
                attrs={
                    "style": "width:100%;",
                }
            ),
        }


class RecordForm(ModelForm):
    class Meta:
        model = Record
        fields = ["date", "title", "content"]
        help_texts = {
            "title": "Changes autosave every 1s.",
            "content": "Default values can be changed on your profile."
            + "  Changes autosave every 1s.",
        }

        widgets = {
            "date": DateInput(
                attrs={
                    "hx-trigger": "change",
                    "hx-post": reverse_lazy("records:change_form"),
                    "hx-target": "#record_update_form",
                    "hx-swap": "outerHTML",
                    "type": "date",
                }
            ),
            "title": Textarea(
                attrs={
                    "hx-trigger": "keyup changed delay:1s",
                    "hx-post": reverse_lazy("records:save_form"),
                    "hx-include": "[name='content'], [name='title'], [name='date']",
                    "style": "height:2.25em;width: calc(75%);",
                }
            ),
            "content": Textarea(
                attrs={
                    "hx-trigger": "keyup changed delay:1s",
                    "hx-post": reverse_lazy("records:save_form"),
                    "hx-include": "[name='content'], [name='title'], [name='date']",
                    "style": "width: calc(100% - 15px);",
                }
            ),
        }
