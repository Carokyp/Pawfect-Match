from django import forms
from django.core.exceptions import ValidationError

from .models import Dog


MAX_PHOTO_SIZE_BYTES = 9.5 * 1024 * 1024  


class DogForm(forms.ModelForm):
    """Form for creating and editing dog profiles."""

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

        # Photo not required when editing an existing dog
        if self.instance and self.instance.pk:
            self.fields["profile_photo"].required = False
            self.fields["profile_photo"].widget.attrs.pop("required", None)

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
            "profile_photo": forms.FileInput(attrs={"accept": "image/*"}),
            "about_me": forms.Textarea(attrs={
                "rows": 4,
                "maxlength": 150,
                "placeholder": (
                    "Tell us about your dog's personality, "
                    "favorite activities etc..."
                ),
            }),
            "name": forms.TextInput(attrs={"placeholder": "e.g., Max"}),
            "breed": forms.TextInput(
                attrs={"placeholder": "e.g., Golden Retriever"}
            ),
            "age": forms.TextInput(
                attrs={"placeholder": "e.g., 3", "type": "number"}
            ),
        }

    def clean_profile_photo(self):
        """Validate profile photo presence and file size."""
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
