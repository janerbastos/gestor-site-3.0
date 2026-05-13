from django import forms
from django.core.exceptions import ValidationError


class ATArquivoCreateForm(forms.Form):
    """
    Formulário responsável pelo cadastro e edição
    de conteúdos do tipo Arquivo.
    """

    titulo = forms.CharField(
        label='Título',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Título do arquivo'
        })
    )

    url = forms.SlugField(
        label='URL (Slug)',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field font-mono',
            'placeholder': 'arquivo-institucional'
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

    descricao = forms.CharField(
        label='Descrição',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'textarea-field',
            'rows': 4,
            'placeholder': 'Descrição resumida do arquivo'
        })
    )

    arquivo_destaque = forms.CharField(
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
        initial=False,
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox-field'
        })
    )

    def clean(self):
        cleaned_data = super().clean()

        arquivo_destaque = cleaned_data.get('arquivo_destaque')

        if not arquivo_destaque:
            raise ValidationError(
                'O documento do arquivo é obrigatório.'
            )

        return cleaned_data


class FactoryATArquivoForm:
    """
    Classe fábrica responsável por retornar
    os formulários do módulo de arquivos.
    """

    _class = {
        'create': ATArquivoCreateForm,
    }

    @classmethod
    def get_class(cls, value):

        try:
            return cls._class[value]

        except KeyError:
            raise ValidationError(
                'Classe de formulário não encontrada.'
            )