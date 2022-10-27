from django import forms
from django.contrib.auth import get_user_model

from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from account.models import Account

User = get_user_model()


class RegisterForm(UserCreationForm):

    fullname = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "inpts",
                "placeholder": "Fullname",
                "size": 30,
            }
        ),
        label="Fullname",
        required=True,
    )
    email = forms.EmailField(
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "inpts",
                "placeholder": "Email",
                "size": 30,
            }
        ),
        label="Email",
        required=True,
    )
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "inpts",
                "placeholder": "Username",
                "size": 30,
            }
        ),
        label="Username",
        required=True,
    )

    referal_code = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "inpts",
                "placeholder": "Referal code (optional)",
                "size": 30,
            }
        ),
        label="Referal code (optional)",
        required=False,
    )

    password1 = forms.CharField(
        max_length=30,
        min_length=6,
        label="Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "inpts", "size": 30}
        ),
    )
    password2 = forms.CharField(
        max_length=30,
        min_length=6,
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Comfirm Password", "class": "inpts", "size": 30}
        ),
    )

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "fullname",
            "password1",
            "password2",
            "referal_code",
        ]

    def clean_referal_code(self):
        refcode = self.cleaned_data["referal_code"]
        if refcode:
            if not Account.objects.filter(unique_id__exact=refcode).exists():
                raise forms.ValidationError("Referal code is invalid")
        return refcode


class LoginForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=80,
        widget=forms.TextInput(
            attrs={"type": "email", "class": "inpts", "placeholder": "Email"}
        ),
        label="Email",
        required=True,
    )
    password = forms.CharField(
        max_length=30,
        min_length=6,
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "inpts",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("email", "password")

    def clean(self):
        if self.is_valid():
            if not authenticate(
                email=self.cleaned_data["email"], password=self.cleaned_data["password"]
            ):
                raise forms.ValidationError("Invalid Username and Password")
