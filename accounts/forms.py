import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from profiles.models import OwnerProfile


class LoginForm(AuthenticationForm):
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
        email = self.cleaned_data.get("email")
        if not User.objects.filter(username=email).exists():
            raise ValidationError("No account found with this email address.")
        return email

    def clean(self):
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
            if not re.search(r"[A-Z]", new_password):
                raise ValidationError(
                    "Password must contain at least one uppercase "
                    "letter (A-Z)."
                )

            if not re.search(r"[0-9]", new_password):
                raise ValidationError(
                    "Password must contain at least one digit (0-9)."
                )

            special_chars = r"[!@#$%^&*()_+\-=\[\]{};:\"\\|,.<>\/?]"
            if not re.search(special_chars, new_password):
                raise ValidationError(
                    "Password must contain at least one special "
                    "character (!@#$%^&*)."
                )

        return cleaned_data


class RegisterForm(forms.Form):
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
        email = self.cleaned_data["email"]
        existing_user = User.objects.filter(username=email).first()
        if existing_user:
            owner_profile = OwnerProfile.objects.filter(user=existing_user).first()
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
        password = self.cleaned_data.get("password")
        if password:
            # Django built-in validators
            try:
                validate_password(password)
            except ValidationError as e:
                raise forms.ValidationError(e.messages)

            # Custom validators
            if not re.search(r'[A-Z]', password):
                raise forms.ValidationError(
                    "Password must contain at least one uppercase "
                    "letter (A–Z)."
                )

            if not re.search(r'[0-9]', password):
                raise forms.ValidationError(
                    "Password must contain at least one digit (0–9)."
                )
            
            special_chars = r'[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]'
            if not re.search(special_chars, password):
                raise forms.ValidationError(
                    "Password must contain at least one special "
                    "character (!@#$%^&*)."
                )

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
