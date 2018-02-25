from django import forms
from django.contrib.auth.models import User

class TokenForm(forms.Form):
    token = forms.CharField(
        required=False,
        label='Token',
        max_length=200
    )
    username = forms.CharField(
        required=False,
        label='Username',
        max_length=200
    )

    class Meta:
        model = User
        fields = ('username',)