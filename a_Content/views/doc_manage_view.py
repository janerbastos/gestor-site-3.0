from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from a_Site.models import FactoryClassModel
from a_Content.forms.doc_form import DocCreateForm
from a_Content.models import ArquivoMidia

def doc_manage_list(request, url):
    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)
    arquivos = site.arquivos.filter(tipo_geral=ArquivoMidia.DOCUMENTO)

    q = request.GET.get('q')
    if q:
        arquivos = arquivos.filter(titulo__icontains=q)


    return render(request, 'content/partials/documento-show.html', {'arquivos': arquivos, 'site': site})


def doc_manage_upload(request, url):
    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)

    form = DocCreateForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        imagem = form.save(commit=False)
        imagem.site = site
        imagem.save()
        return redirect(reverse('content:doc-manage-list', args=(url,)))


    return render(request, 'content/partials/documento-upload.html', {'form': form, 'site': site})


def doc_manage_set(request, url, oid):

    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)

    doc = get_object_or_404(site.arquivos, pk=oid)

    return render(request, 'content/partials/documento-arquivo-set.html', {'site': site, 'doc': doc})
