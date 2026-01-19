from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


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

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
