import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from profiles.models import OwnerProfile


# Regex pattern for allowed special characters in passwords
PASSWORD_SPECIAL_CHARS = r'[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]'


def validate_password_strength(password):
    """
    Validate that a password meets strength requirements.

    Checks for at least one uppercase letter, one digit,
    and one special character.

    Raises:
        ValidationError: If any strength requirement is not met.
    """
    if not re.search(r"[A-Z]", password):
        raise ValidationError(
            "Password must contain at least one uppercase letter (A-Z)."
        )

    if not re.search(r"[0-9]", password):
        raise ValidationError(
            "Password must contain at least one digit (0-9)."
        )

    if not re.search(PASSWORD_SPECIAL_CHARS, password):
        raise ValidationError(
            "Password must contain at least one special character (!@#$%^&*)."
        )


class LoginForm(AuthenticationForm):
    """
    Login form using email instead of username.

    Customizes the default Django authentication form
    with a friendlier error message on failed login.
    """

    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"autocomplete": "username"})
    )
    # Redefined only to add autocomplete attribute for better UX
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"})
    )

    error_messages = {
        "invalid_login": (
            "We couldn't find an account. "
            "Please check your email and password."
        )
    }


class ForgotPasswordForm(forms.Form):
    """
    Password reset form without email verification.

    Validates that the email exists in the database and that
    the new password meets all strength requirements.
    """

    email = forms.EmailField(
        label="Email"
    )

    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )

    new_password_confirm = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )

    def clean_email(self):
        """
        Check that the email belongs to an existing account.

        Raises:
            ValidationError: If no account is found with this email.
        """
        email = self.cleaned_data.get("email")

        if not User.objects.filter(username=email).exists():
            raise ValidationError("No account found with this email address.")

        return email

    def clean(self):
        """
        Check that passwords match and meet strength requirements.

        Raises:
            ValidationError: If passwords don't match or are too weak.
        """
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        new_password_confirm = cleaned_data.get("new_password_confirm")

        if new_password and new_password_confirm:
            if new_password != new_password_confirm:
                raise ValidationError("The two password fields must match.")

            # Run Django's built-in password validators
            try:
                validate_password(new_password)
            except ValidationError as e:
                raise ValidationError(e.messages)

            # Run custom strength validators
            validate_password_strength(new_password)

        return cleaned_data


class RegisterForm(forms.Form):
    """
    Registration form for new users.

    Validates that the email is not already in use and that
    the password meets strength requirements.

    Allows resuming an incomplete registration if the owner
    profile exists but the dog profile is not yet completed.
    """

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"autocomplete": "off"})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )

    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )

    def clean_email(self):
        """
        Check that the email is not already used by a complete account.

        Allows re-registration if the user never finished
        setting up their dog profile.

        Raises:
            ValidationError: If a complete account already exists.
        """
        email = self.cleaned_data["email"]
        existing_user = User.objects.filter(username=email).first()

        if not existing_user:
            return email

        owner_profile = OwnerProfile.objects.filter(
            user=existing_user
        ).first()

        # No owner profile means registration was never started
        if not owner_profile:
            return email

        # Block only if both owner and dog profiles are complete
        if owner_profile.completed:
            has_dog = hasattr(owner_profile, "dog")
            dog_completed = has_dog and owner_profile.dog.completed

            if dog_completed:
                raise forms.ValidationError(
                    "An account with this email already exists. "
                    "Please sign in instead."
                )

        return email

    def clean_password(self):
        """
        Validate password strength using Django and custom validators.

        Raises:
            ValidationError: If the password is too weak.
        """
        password = self.cleaned_data.get("password")

        if password:
            # Run Django's built-in password validators
            try:
                validate_password(password)
            except ValidationError as e:
                raise forms.ValidationError(e.messages)

            # Run custom strength validators
            try:
                validate_password_strength(password)
            except ValidationError as e:
                raise forms.ValidationError(str(e))

        return password

    def clean(self):
        """
        Check that both password fields match.

        Raises:
            ValidationError: If passwords don't match.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
