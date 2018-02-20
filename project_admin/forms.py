from django import forms


class TokenForm(forms.Form):
    token = forms.CharField(
        required=True,
        label='Token',
        max_length=200
    )