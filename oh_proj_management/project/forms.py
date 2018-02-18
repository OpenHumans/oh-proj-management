from django import forms


class TokenForm(forms.Form):
    token = forms.CharField()
