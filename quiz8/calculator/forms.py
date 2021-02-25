import django
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.forms import forms


class EntryForm(forms.Form):
    x_value = forms.IntegerField(required = True, label = "X:")
    y_value = forms.IntegerField(required = True, label="Y:")

    def clean_y(self):
        checkOK = authenticate(self.y_value != 0)
        if not checkOK == 0:
            raise forms.ValidationError("Y == 0!")
        return
