from django import forms
from a_Acl.models import FactoryClassModel

class CreateSiteUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget.attrs.update({'class': 'select-field'})

    class Meta:
        model = FactoryClassModel.get_class('site_role')
        fields = ('user', 'roles')
        widgets = {
            'roles': forms.CheckboxSelectMultiple(),
        }

class EditSiteUserRolesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # O widget já está definido no Meta, mas podemos adicionar classes se necessário
        pass

    class Meta:
        model = FactoryClassModel.get_class('site_role')
        fields = ('roles',)
        widgets = {
            'roles': forms.CheckboxSelectMultiple(),
        }
