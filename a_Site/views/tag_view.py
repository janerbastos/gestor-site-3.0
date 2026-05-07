from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from a_Site.models import FactoryClassModel
from a_Site.forms import TagCreateForm
from a_Account.anotations import PermissionRoot


@PermissionRoot()
def list_tag(request, url):
    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)

    # Assumindo que a relação existe no modelo site ou via generic relation
    tag_list = site.tags.all()

    paginator = Paginator(tag_list, 20)
    page = request.GET.get('page')
    
    try:
        tags = paginator.page(page)
    except PageNotAnInteger:
        tags = paginator.page(1)
    except EmptyPage:
        tags = paginator.page(paginator.num_pages)

    context = {
        'site': site,
        'tags': tags,
        'breadcrumbs': [
            {'label': 'Tags e Categorias', 'url': None}
        ]
    }

    return render(request, 'tag/list_tag.html', context)


@PermissionRoot()
def create_tag(request, url):
    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)
    
    form = TagCreateForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        tag = form.save(commit=False)
        tag.site = site
        tag.save()
        messages.success(request, 'Tag registrada com sucesso.')
        return redirect(reverse('site:list-tag', args=(url,)))
    

    context = {
        'site': site,
        'form': form,
        'breadcrumbs': [
            {'label': 'Tags e Categorias', 'url': reverse('site:list-tag', args=(url,))},
            {'label': 'Nova Tag', 'url': None}
        ]
    }

    return render(request, 'tag/create_tag.html', context)


@PermissionRoot()
def edit_tag(request, url, slug):
    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)
    tag = get_object_or_404(site.tags, tag=slug)

    form = TagCreateForm(request.POST or None, instance=tag)

    if form.is_valid() and request.method == 'POST':
        tag = form.save()
        messages.success(request, 'Tag atualizada com sucesso.')
        return redirect(reverse('site:list-tag', args=(url,)))
    

    context = {
        'site': site,
        'form': form,
        'breadcrumbs': [
            {'label': 'Tags e Categorias', 'url': reverse('site:list-tag', args=(url,))},
            {'label': 'Editar Tag', 'url': None}
        ]
    }

    return render(request, 'tag/edit_tag.html', context)


@PermissionRoot()
def delete_tag(request, url, slug):

    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)
    tag = get_object_or_404(site.tags, tag=slug)

    if request.method == 'POST':
        tag.delete()
        messages.success(request, 'Tag excluída do sistema.')
        return redirect(reverse('site:list-tag', args=(url,)))
    
    context = {
        'tag' : tag,
        'site' : site,
        'breadcrumbs': [
            {'label': 'Tags e Categorias', 'url': reverse('site:list-tag', args=(url,))},
            {'label': 'Ecluir Tag', 'url': None}
        ]
    }

    return render(request, 'tag/delete_tag.html', context)