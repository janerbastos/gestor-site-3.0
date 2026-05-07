from django import forms


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='Senha',
        max_length=100,
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )

    confirmar_password = forms.CharField(
        label='Confirma Nova Senha',
        max_length=100,
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )