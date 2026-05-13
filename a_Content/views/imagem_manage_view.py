from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from a_Site.models import FactoryClassModel
from a_Content.forms.imagam_form import ImagemCreateForm
from a_Content.models import ArquivoMidia


def imagem_manage_list(request, url):
    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)
    arquivos = site.arquivos.filter(tipo_geral=ArquivoMidia.IMAGEM)

    q = request.GET.get('q')
    if q:
        arquivos = arquivos.filter(titulo__icontains=q)


    return render(request, 'content/partials/imagem-show.html', {'arquivos': arquivos, 'site': site})


def imagem_manage_upload(request, url):
    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)

    form = ImagemCreateForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        imagem = form.save(commit=False)
        imagem.site = site
        imagem.save()
        return redirect(reverse('content:imagem-manage-list', args=(url,)))


    return render(request, 'content/partials/imagem-upload.html', {'form': form, 'site': site})


def imagem_manage_set(request, url, oid):

    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)

    imagem = get_object_or_404(site.arquivos, pk=oid)

    return render(request, 'content/partials/imagem-noticia-set.html', {'site': site, 'imagem': imagem})
