import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from profiles.models import OwnerProfile


# Constants
PASSWORD_SPECIAL_CHARS = r'[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]'


def validate_password_strength(password):
    """
    Validate password strength requirements.

    Args:
        password: str. The password to validate.

    Returns:
        None.

    Raises:
        ValidationError if password doesn't contain uppercase letter,
        digit, or special character.
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
    Form for user login with email and password.

    Customizes error messages for better user experience when
    authentication fails.
    """
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "autocomplete": "username"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password"
        })
    )

    error_messages = {
        'invalid_login': (
            "We couldn't find an account. "
            "Please check your email and password."
        )
    }


class ForgotPasswordForm(forms.Form):
    """
    Form for password reset without email verification.

    Validates that the email exists and that the new password meets
    strength requirements before allowing password reset.
    """
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={})
    )

    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password"
        })
    )

    new_password_confirm = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password"
        })
    )

    def clean_email(self):
        """
        Validate that the email has an associated user account.

        Args:
            None.

        Returns:
            str. The validated email address.

        Raises:
            ValidationError if no account is found with the email address.
        """
        email = self.cleaned_data.get("email")
        if not User.objects.filter(username=email).exists():
            raise ValidationError("No account found with this email address.")
        return email

    def clean(self):
        """
        Validate that passwords match and meet strength requirements.

        Args:
            None.

        Returns:
            dict. The cleaned data dictionary.

        Raises:
            ValidationError if passwords don't match or don't meet strength
            requirements (uppercase, digit, and special character).
        """
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        new_password_confirm = cleaned_data.get("new_password_confirm")

        if new_password and new_password_confirm:
            if new_password != new_password_confirm:
                raise ValidationError("The two password fields must match.")

            # Validate password strength
            try:
                validate_password(new_password)
            except ValidationError as e:
                raise ValidationError(e.messages)

            # Custom validators (match registration requirements)
            validate_password_strength(new_password)

        return cleaned_data


class RegisterForm(forms.Form):
    """
    Form for new user registration.

    Validates that email is not already in use and that password meets
    strength requirements. Allows resuming registration if owner profile
    exists without a dog profile.
    """
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "autocomplete": "off"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password"
        })
    )

    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password"
        })
    )

    def clean_email(self):
        """
        Validate that email is not already in use with a complete profile.

        Args:
            None.

        Returns:
            str. The validated email address.

        Raises:
            ValidationError if email is already registered with a dog profile.
        """
        email = self.cleaned_data["email"]
        existing_user = User.objects.filter(username=email).first()
        if existing_user:
            owner_profile = OwnerProfile.objects.filter(
                user=existing_user
            ).first()
            has_dog = False
            if owner_profile:
                has_dog = hasattr(owner_profile, "dog")

            # Allow resume if owner exists without dog
            if has_dog:
                raise forms.ValidationError(
                    "An account with this email already exists."
                )
        return email

    def clean_password(self):
        """
        Validate password strength requirements.

        Args:
            None.

        Returns:
            str. The validated password.

        Raises:
            ValidationError if password doesn't contain uppercase letter,
            digit, or special character.
        """
        password = self.cleaned_data.get("password")
        if password:
            # Django built-in validators
            try:
                validate_password(password)
            except ValidationError as e:
                raise forms.ValidationError(e.messages)

            # Custom validators
            try:
                validate_password_strength(password)
            except ValidationError as e:
                raise forms.ValidationError(str(e))

        return password

    def clean(self):
        """
        Validate that both password fields match.

        Args:
            None.

        Returns:
            dict. The cleaned data dictionary.

        Raises:
            ValidationError if passwords don't match.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
