from django import forms
from django.core.exceptions import ValidationError


class ATEventoCreateForm(forms.Form):
    """
    Formulário responsável pelo cadastro e edição
    de conteúdos do tipo Evento.
    """

    url = forms.SlugField(
        label='URL',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'URL da página'
        })
    )

    titulo = forms.CharField(
        label='Título',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Título do evento'
        })
    )

    descricao = forms.CharField(
        label='Descrição',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'textarea-field',
            'rows': 4,
            'placeholder': 'Resumo do evento'
        })
    )

    corpo = forms.CharField(
        label='Conteúdo',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'textarea-field',
            'rows': 10,
            'placeholder': 'Descrição completa do evento'
        })
    )

    tag = forms.CharField(
        label='Tags',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Palavras-chave separadas por vírgula'
        })
    )

    local = forms.CharField(
        label='Local do Evento',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Ex: Auditório da Ufopa'
        })
    )

    inicio = forms.DateTimeField(
        label='Data/Hora de Início',
        required=False,
        input_formats=[
            '%Y-%m-%d %H:%M',
            '%Y-%m-%dT%H:%M',
        ],
        widget=forms.DateTimeInput(attrs={
            'class': 'input-field',
            'type': 'datetime-local'
        })
    )

    termino = forms.DateTimeField(
        label='Data/Hora de Término',
        required=False,
        input_formats=[
            '%Y-%m-%d %H:%M',
            '%Y-%m-%dT%H:%M',
        ],
        widget=forms.DateTimeInput(attrs={
            'class': 'input-field',
            'type': 'datetime-local'
        })
    )

    participante = forms.CharField(
        label='Participantes',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'textarea-field',
            'rows': 4,
            'placeholder': (
                'Lista de participantes separados por vírgula'
            )
        })
    )

    url_evento = forms.URLField(
        label='Página do Evento',
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'input-field',
            'placeholder': 'https://www.ufopa.edu.br'
        })
    )

    contato = forms.CharField(
        label='Pessoa para Contato',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Ex: Antônio Silva'
        })
    )

    email = forms.EmailField(
        label='E-mail para Contato',
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'input-field',
            'placeholder': 'antonio@ufopa.edu.br'
        })
    )

    telefone = forms.CharField(
        label='Telefone para Contato',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': '(93) 99999-9999'
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

    def clean(self):
        cleaned_data = super().clean()

        inicio = cleaned_data.get('inicio')
        termino = cleaned_data.get('termino')

        if inicio and termino and termino < inicio:
            raise ValidationError(
                'A data de término não pode ser menor que a data de início.'
            )

        return cleaned_data


class FactoryATEventoForm:
    """
    Classe fábrica responsável por retornar
    os formulários do módulo de eventos.
    """

    _class = {
        'create': ATEventoCreateForm,
    }

    @classmethod
    def get_class(cls, value):

        try:
            return cls._class[value]

        except KeyError:
            raise ValidationError(
                'Classe de formulário não encontrada.'
            )