from django import forms
from django.core.exceptions import ValidationError


class ATBannerCreateForm(forms.Form):
    """
    Formulário responsável pelo cadastro e edição
    de conteúdos do tipo Banner.
    """

    CHOICE_TARGET = (
        ('_self', 'Mesma aba'),
        ('_blank', 'Nova aba'),
    )

    titulo = forms.CharField(
        label='Título',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Título do banner'
        })
    )

    url = forms.SlugField(
        label='URL (Slug)',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'banner-principal'
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

    imagem_destaque = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.HiddenInput()
    )

    show_in_menu = forms.BooleanField(
        label='Mostrar no menu',
        initial=False,
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox-field'
        })
    )

    excluir_nav = forms.BooleanField(
        label='Excluir da navegação',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox-field'
        })
    )

    def clean(self):
        cleaned_data = super().clean()

        imagem_destaque = cleaned_data.get('imagem_destaque')

        if not imagem_destaque:
            raise ValidationError(
                'A imagem do banner é obrigatória.'
            )

        return cleaned_data


class FactoryATBannerForm:
    """
    Classe fábrica responsável por retornar
    os formulários do módulo de banner.
    """

    _class = {
        'create': ATBannerCreateForm,
    }

    @classmethod
    def get_class(cls, value):

        try:
            return cls._class[value]

        except KeyError:
            raise ValidationError(
                'Classe de formulário não encontrada.'
            )