from django import forms

from a_Content.models import FactoryClassModel

class ImagemCreateForm(forms.ModelForm):
    titulo = forms.CharField(
        label='Título',
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Título da imagem'})
    )

    slug = forms.SlugField(
        label='URL (Slug)',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'slug-da-imagem'})
    )

    arquivo = forms.ImageField(
        label='Arquivo da imagem',
        required=False,
        help_text='Formatos aceitos: JPG, PNG. Tamanho recomendado: 1200x630px.',
        widget=forms.ClearableFileInput(attrs={'class': 'input-field', 'accept': 'image/*'})
    )

    class Meta:
        model = FactoryClassModel.get_class('midia')
        fields = ('titulo', 'slug', 'arquivo')
