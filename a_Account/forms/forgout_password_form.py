from django import forms

class ForgoutPasswordForm(forms.Form):
    email = forms.EmailField(
        label='E-mail',
        max_length=255,
        widget=forms.EmailInput(attrs={'placeholder': 'exemplo@ufopa.edu.br'})
    )