from django import forms

from a_Site.models import FactoryClassModel

class TagCreateForm(forms.ModelForm):

    class Meta:
        model = FactoryClassModel.get_class('tag')
        fields = ('tag', 'titulo')
        widgets = {
            'tag': forms.TextInput(attrs={
                'class': 'block w-full pl-12 pr-4 py-3 rounded-2xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm bg-slate-50/50',
                'placeholder': 'Slug da tag (ex: noticias-urgentes)'
            }),
            'titulo': forms.TextInput(attrs={
                'class': 'block w-full pl-12 pr-4 py-3 rounded-2xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm bg-slate-50/50',
                'placeholder': 'Título amigável (ex: Notícias Urgentes)'
            }),
        }
