from django import forms
from .models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video

        fields = [
            "title",
            "genre",
            "description",
            "stock",
            "rented",
            "image",
            "release_date",
        ]

        widgets = {
            "release_date": forms.DateInput(attrs={"type": "date"}),
        }
