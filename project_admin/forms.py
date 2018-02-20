from django import forms


class TokenForm(forms.Form):
    #username = forms.CharField(
    #    required=True,
    #    label='Username',
    #    max_length=50
    #)
    token = forms.CharField(
        required=True,
        label='Token',
        max_length=200
    )


class SignUpForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Username',
        max_length=50
    )
    password = forms.CharField(
        required=True,
        label='Password',
        max_length=50,
        widget=forms.PasswordInput()
    )