from django import forms
from .models import Dog


class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = [
            "profile_photo",
            "name",
            "age",
            "breed",
            "size",
            "energy_level",
            "about_me",
        ]

        widgets = {
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
            "age": forms.NumberInput(attrs={
                "placeholder": "e.g., 3",
                "min": 0
            }),
        }
