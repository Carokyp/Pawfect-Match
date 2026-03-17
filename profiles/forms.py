import ast

from django import forms
from django.core.exceptions import ValidationError

from .models import OwnerProfile


# Maximum allowed photo upload size
MAX_PHOTO_SIZE_BYTES = 9.5 * 1024 * 1024

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
    """
    Form for creating and editing owner profiles.

    Handles profile photo requirements, interest selection parsing,
    and form initialization for existing instances.
    """

    interests = forms.MultipleChoiceField(
        required=False,
        choices=INTEREST_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        """Initialize form, set required fields, and parse existing
        interests."""
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

        # Pre-fill interests checkboxes when editing an existing profile
        if not self.data and self.instance and self.instance.interests:
            self.fields["interests"].initial = self._parse_interests(
                self.instance.interests
            )

    @staticmethod
    def _parse_interests(value):
        """
        Parse interests from string, list, or tuple into a cleaned list.

        Handles comma-separated strings and Python list literals.

        Returns:
            list: Cleaned list of interest strings.
        """
        if not value:
            return []

        if isinstance(value, (list, tuple)):
            return [str(item).strip() for item in value if str(item).strip()]

        value = str(value).strip()

        # Handle Python list literal strings like "['Hiking', 'Coffee']"
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

        # Handle comma-separated strings like "Hiking, Coffee"
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
            "profile_photo": forms.FileInput(attrs={"accept": "image/*"}),
            "about_me": forms.Textarea(attrs={
                "rows": 4,
                "maxlength": 150,
                "placeholder": "Tell us about yourself, your lifestyle etc..."
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
        """
        Validate that a profile photo is provided and within size limits.

        Raises:
            ValidationError: If photo is missing or exceeds 9.5 MB.
        """
        photo = self.cleaned_data.get("profile_photo")
        photo_removed = self.data.get("profile_photo_removed") == "1"
        existing_photo = (
            self.instance.profile_photo
            if self.instance and self.instance.pk
            else None
        )

        if photo_removed:
            raise ValidationError("Please select a profile photo.")

        if photo:
            # Validate size only when available — some Cloudinary backends
            # don't expose a local .size attribute
            photo_size = getattr(photo, "size", None)
            if (
                isinstance(photo_size, (int, float))
                and photo_size > MAX_PHOTO_SIZE_BYTES
            ):
                size_mb = photo_size / (1024 * 1024)
                raise ValidationError(
                    f"File too large ({size_mb:.1f} MB). "
                    "Maximum size is 9.5 MB. "
                    "Please use a smaller or compressed image."
                )
            return photo

        if existing_photo:
            return existing_photo

        raise ValidationError("Please select a profile photo.")

    def save(self, commit=True):
        """
        Save the form instance and convert interests list to
        a comma-separated string for database storage.
        """
        instance = super().save(commit=False)
        interests = self.cleaned_data.get("interests")

        # Convert list to comma-separated string for CharField storage
        if isinstance(interests, (list, tuple)):
            instance.interests = ", ".join(interests)
        elif interests is None:
            instance.interests = ""

        if commit:
            instance.save()

        return instance
