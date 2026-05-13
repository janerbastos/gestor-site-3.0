from django import forms
from django.core.exceptions import ValidationError
from a_Content.models import ContentViewerMode

class ATViewerCreateForm(forms.Form):
    """
    Formulário responsável pelo cadastro
    de conteúdos do tipo Visão.
    """


    url = forms.SlugField(
        label='URL (Slug)',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'pagina-de-visao'
        })
    )

    titulo = forms.CharField(
        label='Título',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Título da visão'
        })
    )

    descricao = forms.CharField(
        label='Descrição',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'textarea-field',
            'rows': 4,
            'placeholder': 'Resumo ou descrição da visão'
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

    viewer_mode = forms.ChoiceField(
        label='Modo de Visualização',
        choices=ContentViewerMode.CHOICES,
        initial=ContentViewerMode.CHILDREN,
        widget=forms.Select(attrs={
            'class': 'select-field'
        })
    )

    target_path = forms.CharField(
        label='Caminho do Conteúdo',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field font-mono',
            'placeholder': '/noticias/ ou /eventos/'
        })
    )

    template_name = forms.CharField(
        label='Template Customizado',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field font-mono',
            'placeholder': 'content/views/timeline.html'
        })
    )

    ordering = forms.CharField(
        label='Ordenação',
        max_length=100,
        required=False,
        initial='-public_at',
        widget=forms.TextInput(attrs={
            'class': 'input-field font-mono',
            'placeholder': '-public_at'
        })
    )

    limit = forms.IntegerField(
        label='Limite de Registros',
        required=False,
        min_value=1,
        initial=10,
        widget=forms.NumberInput(attrs={
            'class': 'input-field',
            'placeholder': '10'
        })
    )

    show_in_menu = forms.BooleanField(
        label='Mostrar no menu',
        initial=True,
        required=False,
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

    def clean(self):
        cleaned_data = super().clean()

        viewer_mode = cleaned_data.get('viewer_mode')
        target_path = cleaned_data.get('target_path')

        if viewer_mode in ['redirect', 'proxy', 'children', 'timeline', 'gallery']:
            if not target_path:
                raise ValidationError(
                    'Informe o caminho do conteúdo alvo.'
                )

        return cleaned_data


class FactoryATViewerForm:
    """
    Classe fábrica responsável por retornar
    os formulários do módulo de visão.
    """

    _class = {
        'create': ATViewerCreateForm,
    }

    @classmethod
    def get_class(cls, value):

        try:
            return cls._class[value]

        except KeyError:
            raise ValidationError(
                'Classe de formulário não encontrada.'
            )