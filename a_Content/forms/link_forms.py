from django import forms
from django.core.exceptions import ValidationError


class ATLinkCreateForm(forms.Form):
    """
    Formulário responsável pelo cadastro e edição
    de conteúdos do tipo Link.
    """

    CHOICE_TARGET = (
        ('_self', 'Mesma aba'),
        ('_blank', 'Nova aba'),
    )

    url = forms.SlugField(
        label='URL',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'URL amigável do link'
        })
    )

    titulo = forms.CharField(
        label='Título',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Título do link'
        })
    )

    link = forms.URLField(
        label='Link Externo',
        max_length=255,
        widget=forms.URLInput(attrs={
            'class': 'input-field',
            'placeholder': 'https://www.ufopa.edu.br'
        })
    )

    target = forms.ChoiceField(
        label='Destino do Link',
        choices=CHOICE_TARGET,
        initial='_blank',
        widget=forms.Select(attrs={
            'class': 'select-field'
        })
    )

    tag = forms.CharField(
        label='Tags',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': (
                'Palavras-chave separadas por vírgula'
            )
        })
    )

    show_in_menu = forms.BooleanField(
        label='Mostrar no menu',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox-field'
        })
    )

    excluir_nav = forms.BooleanField(
        label='Excluir da navegação',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox-field'
        })
    )


class FactoryATLinkForm:
    """
    Classe fábrica responsável pelos
    formulários do módulo Link.
    """

    _class = {
        'create': ATLinkCreateForm,
    }

    @classmethod
    def get_class(cls, value):

        try:
            return cls._class[value]

        except KeyError:

            raise ValidationError(
                'Classe de formulário não encontrada.'
            )