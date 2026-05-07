from django import forms

from a_Site.models import FactoryClassModel


class CreateSiteForm(forms.ModelForm):

    class Meta:
        model = FactoryClassModel.get_class('site')
        fields = ['url', 'titulo', 'descricao', 'status', 'workflow']
        widgets = {
            'url': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm',
                'placeholder': 'ex: meusite.com.br'
            }),
            'titulo': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm',
                'placeholder': 'Título do Site'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'block w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm',
                'placeholder': 'Uma breve descrição sobre o portal...',
                'rows': 4
            }),
            'status': forms.Select(attrs={
                'class': 'block w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm'
            }),
            'workflow': forms.Select(attrs={
                'class': 'block w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm'
            }),
        }