from django import forms

from a_Site.models import FactoryClassModel

class MidiaSiteForm(forms.ModelForm):

    class Meta:
        model = FactoryClassModel.get_class('site')
        fields = ('favicon', 'logo', 'banner_topo')


class RedeSocialSiteForm(forms.ModelForm):

    class Meta:
        model = FactoryClassModel.get_class('site')
        fields = ('facebook_link', 'twitter_link', 'youtube_link', 'google_link', 'flicker_link', 'rss_link')
        widgets = {
            'facebook_link': forms.URLInput(attrs={
                'class': 'block w-full pl-12 pr-4 py-3 rounded-2xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm bg-slate-50/50',
                'placeholder': 'https://facebook.com/seu-perfil'
            }),
            'twitter_link': forms.URLInput(attrs={
                'class': 'block w-full pl-12 pr-4 py-3 rounded-2xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm bg-slate-50/50',
                'placeholder': 'https://twitter.com/seu-perfil'
            }),
            'youtube_link': forms.URLInput(attrs={
                'class': 'block w-full pl-12 pr-4 py-3 rounded-2xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm bg-slate-50/50',
                'placeholder': 'https://youtube.com/seu-canal'
            }),
            'google_link': forms.URLInput(attrs={
                'class': 'block w-full pl-12 pr-4 py-3 rounded-2xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm bg-slate-50/50',
                'placeholder': 'https://plus.google.com/seu-perfil'
            }),
            'flicker_link': forms.URLInput(attrs={
                'class': 'block w-full pl-12 pr-4 py-3 rounded-2xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm bg-slate-50/50',
                'placeholder': 'https://flickr.com/seu-perfil'
            }),
            'rss_link': forms.URLInput(attrs={
                'class': 'block w-full pl-12 pr-4 py-3 rounded-2xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm bg-slate-50/50',
                'placeholder': 'https://meusite.com/feed/'
            }),
        }


class CodigoScriptSiteForm(forms.ModelForm):

    class Meta:
        model = FactoryClassModel.get_class('site')
        fields = ('facebook_cod', 'twitter_cod', 'youtube_cod', 'google_cod', 'flicker_cod', 'analytic_cod', 'html_cod')
        widgets = {
            'facebook_cod': forms.Textarea(attrs={
                'class': 'block w-full px-4 py-3 rounded-2xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-xs font-mono bg-slate-50/50',
                'placeholder': '<!-- Cole o código do Facebook Pixel ou SDK aqui -->',
                'rows': 4
            }),
            'twitter_cod': forms.Textarea(attrs={
                'class': 'block w-full px-4 py-3 rounded-2xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-xs font-mono bg-slate-50/50',
                'placeholder': '<!-- Cole o código de acompanhamento do Twitter aqui -->',
                'rows': 4
            }),
            'youtube_cod': forms.Textarea(attrs={
                'class': 'block w-full px-4 py-3 rounded-2xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-xs font-mono bg-slate-50/50',
                'placeholder': '<!-- Cole o código de incorporação do YouTube aqui -->',
                'rows': 4
            }),
            'google_cod': forms.Textarea(attrs={
                'class': 'block w-full px-4 py-3 rounded-2xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-xs font-mono bg-slate-50/50',
                'placeholder': '<!-- Cole códigos relacionados ao Google Search Console ou outros -->',
                'rows': 4
            }),
            'flicker_cod': forms.Textarea(attrs={
                'class': 'block w-full px-4 py-3 rounded-2xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-xs font-mono bg-slate-50/50',
                'placeholder': '<!-- Cole o código do Flickr aqui -->',
                'rows': 4
            }),
            'analytic_cod': forms.Textarea(attrs={
                'class': 'block w-full px-4 py-3 rounded-2xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-xs font-mono bg-slate-50/50',
                'placeholder': '<!-- Cole o Global Site Tag (gtag.js) do Google Analytics aqui -->',
                'rows': 4
            }),
            'html_cod': forms.Textarea(attrs={
                'class': 'block w-full px-4 py-3 rounded-2xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-xs font-mono bg-slate-50/50',
                'placeholder': '<!-- Cole qualquer outro código HTML/JS customizado para o <head> ou <body> -->',
                'rows': 6
            }),
        }


class ContentTypeSiteForm(forms.ModelForm):

    class Meta:
        model = FactoryClassModel.get_class('site')
        fields = ('tipos_conteudo', )
        widgets = {
            'tipos_conteudo': forms.CheckboxSelectMultiple(attrs={
                'class': 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4',
            }),
        }


class EnderecoSiteForm(forms.ModelForm):

    class Meta:
        model = FactoryClassModel.get_class('site')
        fields = ('texto_rodape', 'email', 'telefone')
        widgets = {
            'texto_rodape': forms.Textarea(attrs={
                'class': 'block w-full px-4 py-3 rounded-2xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm bg-slate-50/50',
                'placeholder': 'Digite as informações que aparecerão no rodapé do site...',
                'rows': 4
            }),
            'email': forms.EmailInput(attrs={
                'class': 'block w-full pl-12 pr-4 py-3 rounded-2xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm bg-slate-50/50',
                'placeholder': 'contato@exemplo.com.br'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'block w-full pl-12 pr-4 py-3 rounded-2xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm bg-slate-50/50',
                'placeholder': '(00) 0000-0000'
            }),
        }