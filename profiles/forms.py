from django import forms
from .models import OwnerProfile


class OwnerProfileForm(forms.ModelForm):
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
            "about_me": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": (
                    "Tell us about yourself, your lifestyle, and "
                    "what you're looking for in a dog playdate..."
                )
            }),
            "interests": forms.TextInput(attrs={
                "placeholder": "e.g., Hiking, Coffee, Photography"
            }),
            "name": forms.TextInput(attrs={
                "placeholder": "e.g., Sarah"
            }),
            "city": forms.TextInput(attrs={
                "placeholder": "e.g., San Francisco"
            }),
            "age": forms.NumberInput(attrs={
                "placeholder": "e.g., 28",
                "min": 18
            }),
        }
