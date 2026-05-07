from django import forms
from django.contrib import auth

class CreateUserForm(forms.ModelForm):

    class Meta:
        model = auth.get_user_model()
        fields = ['first_name', 'last_name', 'email', 'is_active']