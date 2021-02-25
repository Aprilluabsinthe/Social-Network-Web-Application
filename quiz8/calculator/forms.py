import django
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django import forms


class EntryForm(forms.Form):
    x = forms.IntegerField(label="X:")
    y = forms.IntegerField(label="Y:")

    def clean_y(self):
        y = self.cleaned_data.get("y")
        if y == 0:
            raise forms.ValidationError("Y == 0!!!!")
        return y
