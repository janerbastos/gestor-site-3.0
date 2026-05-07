from django import forms
from django.core.exceptions import ValidationError


class ATPaginaCreateForm(forms.Form):

    url = forms.SlugField(max_length=255)
    titulo = forms.CharField(max_length=255)
    descricao = forms.CharField(
        required=False,
        label='Descrição',
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Sumário da pagina'
        }))
    corpo = forms.CharField(
        required=False,
        label='Corpo da página',
        widget=forms.Textarea(attrs={
            'rows': 10,
            'placeholder': 'Corpo da pagina'
        }))
    show_in_menu = forms.BooleanField(
        label="Mostrar no menu",
        required=False
    )
    excluir_nav = forms.BooleanField(
        label="Excluir da navegação",
        required=False
    )



# Metodo fabrica
class FactoryATPageForm:

    _class = {
        'create': ATPaginaCreateForm,

    }

    @classmethod
    def get_class(cls, value):

        try:
            return cls._class[value]
        except KeyError:
            raise ValidationError('Classe não encontrada')