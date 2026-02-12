import ast
from django import forms
from django.core.exceptions import ValidationError
from .models import OwnerProfile


INTEREST_CHOICES = [
    ("Hiking", "Hiking"),
    ("Coffee", "Coffee"),
    ("Photography", "Photography"),
    ("Travel", "Travel"),
    ("Cooking", "Cooking"),
    ("Movies", "Movies"),
    ("Music", "Music"),
    ("Reading", "Reading"),
    ("Fitness", "Fitness"),
    ("Yoga", "Yoga"),
    ("Gaming", "Gaming"),
    ("Art", "Art"),
    ("Dancing", "Dancing"),
    ("Foodie", "Foodie"),
    ("Comedie", "Comedie"),
    ("Bars", "Bars"),
]


class OwnerProfileForm(forms.ModelForm):
    interests = forms.MultipleChoiceField(
        required=False,
        choices=INTEREST_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )

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
        if self.instance and self.instance.pk:
            self.fields["profile_photo"].required = False
            self.fields["profile_photo"].widget.attrs.pop("required", None)

        if not self.data and self.instance and self.instance.interests:
            self.fields["interests"].initial = self._parse_interests(
                self.instance.interests
            )

    @staticmethod
    def _parse_interests(value):
        if not value:
            return []
        if isinstance(value, (list, tuple)):
            return [str(item).strip() for item in value if str(item).strip()]
        value = str(value).strip()
        if value.startswith("[") and value.endswith("]"):
            try:
                parsed = ast.literal_eval(value)
            except (ValueError, SyntaxError):
                parsed = None
            if isinstance(parsed, (list, tuple)):
                return [
                    str(item).strip()
                    for item in parsed
                    if str(item).strip()
                ]
        return [item.strip() for item in value.split(",") if item.strip()]

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
                "maxlength": 150,
                "placeholder": (
                    "Tell us about yourself, your lifestyle ect..."
                )
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
        if not photo and self.instance and self.instance.pk:
            return self.instance.profile_photo
        if not photo:
            raise ValidationError("Please select a profile photo.")
        return photo

    def save(self, commit=True):
        instance = super().save(commit=False)
        interests = self.cleaned_data.get("interests")
        if isinstance(interests, (list, tuple)):
            instance.interests = ", ".join(interests)
        elif interests is None:
            instance.interests = ""
        if commit:
            instance.save()
        return instance

