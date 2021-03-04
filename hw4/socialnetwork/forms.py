from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class ProfileForm(forms.Form):
    last_name = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)
    birthday = forms.DateField(required=False)
    children = forms.IntegerField(required=False, label='# of children')
    address = forms.CharField(required=False, max_length=200)
    city = forms.CharField(required=False, max_length=30)
    state = forms.CharField(required=False, max_length=20)
    zip_code = forms.CharField(required=False, max_length=10)
    country = forms.CharField(required=False, max_length=30)
    email = forms.CharField(required=False, max_length=32)
    phone_number = forms.CharField(required=False, max_length=16, label='Phone #')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label='Username')
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(), label="Password")

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")
        return cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, label="Username")
    password = forms.CharField(max_length=200,
                               label='Password',
                               widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=200,
                                       label='Confirm',
                                       widget=forms.PasswordInput())
    email = forms.CharField(max_length=50,
                            widget=forms.EmailInput(), label='E-mail')
    first_name = forms.CharField(max_length=20, label='First Name')
    last_name = forms.CharField(max_length=20, label='Last Name')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username
