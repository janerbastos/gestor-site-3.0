from django import forms
from django.core.exceptions import ValidationError


class ATAgendaCreateForm(forms.Form):
    """
    Formulário responsável pelo cadastro e edição
    de conteúdos do tipo Agenda.
    """

    url = forms.SlugField(
        label='URL',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'URL da agenda'
        })
    )

    titulo = forms.CharField(
        label='Título',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Título da agenda'
        })
    )

    descricao = forms.CharField(
        label='Descrição',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'textarea-field',
            'rows': 4,
            'placeholder': 'Resumo da agenda'
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
        label='Local',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Ex: Reitoria UFOPA'
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

    responsavel = forms.CharField(
        label='Responsável',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Ex: Marcelo Felipe'
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

    cor = forms.CharField(
        label='Cor de destaque',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Ex: #4f46e5'
        })
    )

    dia_todo = forms.BooleanField(
        label='Dia todo',
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox-field'
        })
    )

    observacao = forms.CharField(
        label='Observações',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'textarea-field',
            'rows': 4,
            'placeholder': (
                'Ex: Levar relatório acadêmico'
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

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('inicio')
        termino = cleaned_data.get('termino')

        if inicio and termino and termino < inicio:
            raise ValidationError(
                'A data de término não pode ser menor que a data de início.'
            )
        return cleaned_data


class FactoryATAgendaForm:
    """
    Classe fábrica responsável pelos
    formulários do módulo Agenda.
    """
    _class = {
        'create': ATAgendaCreateForm,
    }

    @classmethod
    def get_class(cls, value):
        try:
            return cls._class[value]
        except KeyError:
            raise ValidationError(
                'Classe de formulário não encontrada.'
            )