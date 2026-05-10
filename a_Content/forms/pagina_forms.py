from django import forms
from django.core.exceptions import ValidationError


class ATPaginaCreateForm(forms.Form):

    url = forms.SlugField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'URL da página'
        })
    )
    titulo = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Título da página'
        })
    )
    descricao = forms.CharField(
        required=False,
        label='Descrição',
        widget=forms.Textarea(attrs={
            'class': 'textarea-field',
            'rows': 4,
            'placeholder': 'Sumário da página'
        })
    )
    corpo = forms.CharField(
        required=False,
        label='Corpo da página',
        widget=forms.Textarea(attrs={
            'class': 'textarea-field',
            'rows': 10,
            'placeholder': 'Corpo da página'
        })
    )
    tag = forms.CharField(
        label='Tags',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field', 
            'placeholder': 'Palavras-chave separadas por vírgula'
        })
    )
    show_in_menu = forms.BooleanField(
        label="Mostrar no menu",
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox-field'
        })
    )
    excluir_nav = forms.BooleanField(
        label="Excluir da navegação",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox-field'
        })
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