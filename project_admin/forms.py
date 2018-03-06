from django import forms


class TokenForm(forms.Form):
    token = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
