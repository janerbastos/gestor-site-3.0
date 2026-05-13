from django import forms
from django.core.exceptions import ValidationError

from a_Content.models import FactoryClassModel


class DocCreateForm(forms.ModelForm):
    """
    Formulário responsável pelo cadastro
    de documentos e arquivos.
    """

    titulo = forms.CharField(
        label='Título',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Título do documento'
        })
    )

    slug = forms.SlugField(
        label='URL (Slug)',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'documento-institucional'
        })
    )

    arquivo = forms.FileField(
        label='Arquivo do Documento',
        required=True,
        help_text=(
            'Formatos aceitos: PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX. '
            'Tamanho máximo recomendado: 5MB.'
        ),
        widget=forms.ClearableFileInput(attrs={
            'class': 'input-field',
            'accept': (
                '.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,'
                '.odt,.ods,.odp'
            )
        })
    )

    class Meta:
        model = FactoryClassModel.get_class('midia')
        fields = (
            'titulo',
            'slug',
            'arquivo',
        )

    def clean_arquivo(self):

        arquivo = self.cleaned_data.get('arquivo')

        if not arquivo:
            raise ValidationError(
                'O arquivo do documento é obrigatório.'
            )

        allowed_extensions = [
            '.pdf',
            '.doc',
            '.docx',
            '.xls',
            '.xlsx',
            '.ppt',
            '.pptx',
            '.odt',
            '.ods',
            '.odp',
        ]

        filename = arquivo.name.lower()

        if not any(filename.endswith(ext) for ext in allowed_extensions):
            raise ValidationError(
                'Formato de arquivo não suportado.'
            )

        return arquivo