from django import forms
from django.core.exceptions import ValidationError


class ATPastaCreateForm(forms.Form):

    url = forms.SlugField(max_length=255, required=False)
    titulo = forms.CharField(max_length=255)
    descricao = forms.CharField(
        required=False,
        label='Descrição',
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Sumário da pasta'
        }))
    show_in_menu = forms.BooleanField(
        label="Mostrar no menu",
        initial=True,
        required=False
    )
    excluir_nav = forms.BooleanField(
        label="Excluir da navegação",
        required=False
    )



# Metodo fabrica
class FactoryATPastaForm:

    _class = {
        'create': ATPastaCreateForm,

    }

    @classmethod
    def get_class(cls, value):

        try:
            return cls._class[value]
        except KeyError:
            raise ValidationError('Classe não encontrada')