from django import forms

from a_Acl.models import FactoryClassModel

class CreateRoleForm(forms.ModelForm):

    class Meta:
        model = FactoryClassModel.get_class('role')
        fields = ['nome', 'slug', 'level']