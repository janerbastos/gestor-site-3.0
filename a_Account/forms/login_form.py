from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Usuário',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu usuário'})
    )
    password = forms.CharField(
        label='Senha',
        max_length=100,
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )