from django import forms
from django.core.exceptions import ValidationError


class ATServicoCreateForm(forms.Form):
    """
    Formulário responsável pelo cadastro e edição
    de conteúdos do tipo Serviço.
    """

    url = forms.SlugField(
        label='URL',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'URL do serviço'
        })
    )

    titulo = forms.CharField(
        label='Título',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Título do serviço'
        })
    )

    descricao = forms.CharField(
        label='Descrição',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'textarea-field',
            'rows': 4,
            'placeholder': 'Resumo do serviço'
        })
    )

    corpo = forms.CharField(
        label='Requisitos do Serviço',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'textarea-field',
            'rows': 10,
            'placeholder': (
                'Descreva os requisitos para '
                'solicitação do serviço'
            )
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

    # Metadata
    quem_pode = forms.CharField(
        label='Quem pode solicitar',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': (
                'Ex: Servidores, docentes e técnicos'
            )
        })
    )

    como_solicitar = forms.CharField(
        label='Como solicitar',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'textarea-field',
            'rows': 5,
            'placeholder': (
                'Ex: Abrir chamado no GLPI '
                'ou enviar solicitação institucional'
            )
        })
    )

    prazo = forms.CharField(
        label='Prazo de atendimento',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Ex: 24 horas úteis'
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


class FactoryATServicoForm:
    """
    Classe fábrica responsável pelos
    formulários do módulo Serviço.
    """

    _class = {
        'create': ATServicoCreateForm,
    }

    @classmethod
    def get_class(cls, value):

        try:
            return cls._class[value]

        except KeyError:

            raise ValidationError(
                'Classe de formulário não encontrada.'
            )