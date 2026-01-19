from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import re


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
        if User.objects.filter(username=email).exists():
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
            
            if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]', password):
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
