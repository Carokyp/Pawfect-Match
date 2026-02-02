from django import forms
from django.core.exceptions import ValidationError
from .models import Dog


class DogForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = [
            "profile_photo",
            "name",
            "age",
            "breed",
            "size",
            "gender",
            "energy_level",
        ]
        for field_name in required_fields:
            field = self.fields.get(field_name)
            if field:
                field.required = True
                field.widget.attrs["required"] = "required"

    class Meta:
        model = Dog
        fields = [
            "profile_photo",
            "name",
            "age",
            "breed",
            "size",
            "gender",
            "energy_level",
            "about_me",
        ]

        widgets = {
            "profile_photo": forms.FileInput(attrs={
                "accept": "image/*"
            }),
            "about_me": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": (
                    "Tell us about your dog's personality, "
                    "favorite activities etc..."
                )
            }),
            "name": forms.TextInput(attrs={
                "placeholder": "e.g., Max"
            }),
            "breed": forms.TextInput(attrs={
                "placeholder": "e.g., Golden Retriever"
            }),
            "age": forms.TextInput(attrs={
                "placeholder": "e.g., 3",
                "type": "number"
            }),
        }

    def clean_profile_photo(self):
        photo = self.cleaned_data.get("profile_photo")
        if not photo:
            raise ValidationError("Please select a profile photo.")
        return photo
