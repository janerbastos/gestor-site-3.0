from django import forms
from django.core.exceptions import ValidationError


class ATInformeCreateForm(forms.Form):
    titulo = forms.CharField(
        label='Título',
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Título do informe.'})
    )
    url = forms.SlugField(
        label='URL (Slug)',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'ex: url-da-informe'})
    )
    descricao = forms.CharField(
        label='Descrição',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'textarea-field',
            'rows': 3,
            'placeholder': 'Sumário ou breve descrição do informe'
        })
    )
    tag = forms.CharField(
        label='Tags',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Palavras-chave separadas por vírgula'})
    )
    legenda_imagem = forms.CharField(
        label='Legenda da Imagem',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Texto de citação da imagem'})
    )
    corpo = forms.CharField(
        label='Corpo da Notícia',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'textarea-field',
            'rows': 10,
            'placeholder': 'Escreva o conteúdo completo aqui...'
        })
    )
    show_imagem = forms.BooleanField(
        label="Visualizar imagem na listagem",
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'checkbox-field'})
    )
    show_in_menu = forms.BooleanField(
        label="Mostrar no menu",
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'checkbox-field'})
    )
    excluir_nav = forms.BooleanField(
        label="Excluir da navegação",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'checkbox-field'})
    )



# Metodo fabrica
class FactoryATInformeForm:

    _class = {
        'create': ATInformeCreateForm,

    }

    @classmethod
    def get_class(cls, value):

        try:
            return cls._class[value]
        except KeyError:
            raise ValidationError('Classe não encontrada')