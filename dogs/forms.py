from django import forms
from django.core.exceptions import ValidationError

from .models import Dog


class DogForm(forms.ModelForm):
    """
    Form for creating and editing dog profiles.

    Dynamically sets required fields and validates profile photo presence.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize DogForm and set required field constraints.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments passed to parent form.
        """
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
            "profile_photo": forms.FileInput(attrs={
                "accept": "image/*"
            }),
            "about_me": forms.Textarea(attrs={
                "rows": 4,
                "maxlength": 150,
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
        """
        Validate that a profile photo is provided and file size is
        within limits.

        Args:
            None.

        Returns:
            CloudinaryField instance. The validated profile photo.

        Raises:
            ValidationError if no profile photo is provided, instance is new,
                or file size exceeds 9.5 MB.
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
            # Strict file size validation (9.5 MB to have some buffer)
            MAX_FILE_SIZE_BYTES = 9.5 * 1024 * 1024
            if photo.size > MAX_FILE_SIZE_BYTES:
                size_mb = photo.size / (1024 * 1024)
                raise ValidationError(
                    f"File too large ({size_mb:.1f} MB). "
                    "Maximum size is 9.5 MB. "
                    "Please use a smaller or compressed image."
                )
            return photo
        if existing_photo:
            return existing_photo

        raise ValidationError("Please select a profile photo.")
