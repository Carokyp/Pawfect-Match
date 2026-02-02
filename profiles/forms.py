from django import forms
from django.core.exceptions import ValidationError
from .models import OwnerProfile


class OwnerProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = [
            "profile_photo",
            "name",
            "age",
            "city",
            "occupation",
        ]
        for field_name in required_fields:
            field = self.fields.get(field_name)
            if field:
                field.required = True
                field.widget.attrs["required"] = "required"
    class Meta:
        model = OwnerProfile
        fields = [
            "profile_photo",
            "name",
            "age",
            "city",
            "occupation",
            "interests",
            "about_me",
        ]

        widgets = {
            "profile_photo": forms.FileInput(attrs={
                "accept": "image/*"
            }),
            "about_me": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": (
                    "Tell us about yourself, your lifestyle ect..."
                )
            }),
            "interests": forms.TextInput(attrs={
                "placeholder": "e.g., Hiking, Coffee, Photography"
            }),
            "occupation": forms.TextInput(attrs={
                "placeholder": "e.g., Software Engineer"
            }),
            "name": forms.TextInput(attrs={
                "placeholder": "e.g., Sarah"
            }),
            "city": forms.TextInput(attrs={
                "placeholder": "e.g., San Francisco"
            }),
            "age": forms.TextInput(attrs={
                "placeholder": "e.g., 28",
                "type": "number"
            }),
        }

    def clean_profile_photo(self):
        photo = self.cleaned_data.get("profile_photo")
        if not photo:
            raise ValidationError("Please select a profile photo.")
        return photo
