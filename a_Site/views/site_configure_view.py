from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse


from a_Site.models import FactoryClassModel
from a_Site.forms import (
    MidiaSiteForm, RedeSocialSiteForm, CodigoScriptSiteForm,
    ContentTypeSiteForm, EnderecoSiteForm)


def edit_site_midia(request, url):
    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)

    form = MidiaSiteForm(request.POST or None, request.FILES or None, instance=site)

    if form.is_valid() and request.method == 'POST':
        form.save()
        messages.success(request, 'Arquivos de mídia atualizados com sucesso.')
        return redirect(reverse('site:edit-site-midia', args=(url,)))
    
    context = {
        'form' : form,
        'site' : site,
        'breadcrumbs': [
            {'label': 'Mídia e Arquivos', 'url': None}
        ]
    }

    return render(request, 'site/edit_site_midia.html', context)


def edit_site_redesocial_link(request, url):
    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)

    form = RedeSocialSiteForm(request.POST or None, instance=site)

    if form.is_valid() and request.method == 'POST':
        form.save()
        messages.success(request, 'Link de Rede Socias atualizadas com sucesso.')
        return redirect(reverse('site:edit-site-redesocial-link', args=(url,)))

    context = {
        'form' : form,
        'site' : site,
        'breadcrumbs': [
            {'label': 'Redes Sociais', 'url': None}
        ]
    }

    return render(request, 'site/edit_site_redesocial_link.html', context)


def edit_site_codigo_script(request, url):
    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)

    form = CodigoScriptSiteForm(request.POST or None, instance=site)

    if form.is_valid() and request.method == 'POST':
        form.save()
        messages.success(request, 'Codigo de Rede Socias atualizadas com sucesso.')
        return redirect(reverse('site:edit-site-codigo-script', args=(url,)))

    context = {
        'form' : form,
        'site' : site,
        'breadcrumbs': [
            {'label': 'Código e Script', 'url': None}
        ]
    }

    return render(request, 'site/edit_site_codigo_script.html', context)


def edit_site_contenttype(request, url):
    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)

    form = ContentTypeSiteForm(request.POST or None, instance=site)

    if form.is_valid() and request.method == 'POST':
        form.save()
        messages.success(request, 'Contéudo atualizado.')
        return redirect(reverse('site:edit-site-content-type', args=(url,)))

    context = {
        'form' : form,
        'site' : site,
        'breadcrumbs': [
            {'label': 'Tipo de Conteúdo', 'url': None}
        ]
    }

    return render(request, 'site/edit_site_contenttype.html', context)


def edit_site_endereco(request, url):
    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)

    form = EnderecoSiteForm(request.POST or None, instance=site)

    if form.is_valid() and request.method == 'POST':
        form.save()
        messages.success(request, 'Endereço atualizado.')
        return redirect(reverse('site:edit-site-endereco', args=(url,)))

    context = {
        'form' : form,
        'site' : site,
        'breadcrumbs': [
            {'label': 'Endereço', 'url': None}
        ]
    }

    return render(request, 'site/edit_site_endereco.html', context)