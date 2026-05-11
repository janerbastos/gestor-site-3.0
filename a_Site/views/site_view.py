from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from a_Site.models import FactoryClassModel
from a_Site.forms import CreateSiteForm
from a_Account.anotations import PermissionRoot



@PermissionRoot()
def dashboard(request):
    Site = FactoryClassModel.get_class('site')
    site_list = Site.objects.all()

    search_query = request.GET.get('q')
    if search_query:
        from django.db.models import Q
        site_list = site_list.filter(
            Q(titulo__icontains=search_query) |
            Q(descricao__icontains=search_query) | 
            Q(url__icontains=search_query)
        )

    paginator = Paginator(site_list, 20)
    page = request.GET.get('page')
    
    try:
        sites = paginator.page(page)
    except PageNotAnInteger:
        sites = paginator.page(1)
    except EmptyPage:
        sites = paginator.page(paginator.num_pages)

    context = {
        'sites' : sites,
        'breadcrumbs': [],
    }

    return render(request, 'site/dashboard.html', context)


@PermissionRoot()
def create_site(request):
    form = CreateSiteForm(request.POST or None)
    user = request.user

    if form.is_valid() and request.method == 'POST':
        site = form.save(commit=False)
        site.dono = user
        site.save()
        messages.success(request, 'Site registrado com sucesso.')
        return redirect('site:dashboard')
    
    context = {
        'form' : form,
        'breadcrumbs': [
            {'label': 'Novo Site', 'url': None}
        ]
    }

    return render(request, 'site/create_site.html', context)


@PermissionRoot()
def open_site(request, url):
    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)

    context = {
        'site' : site,
        'breadcrumbs': [
            {'label': site.titulo, 'url': None}
        ]
    }

    return render(request, 'site/open_site.html', context)


@PermissionRoot()
def edit_site(request, url):
    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)

    form = CreateSiteForm(request.POST or None, instance=site)

    if form.is_valid() and request.method == 'POST':
        form.save()
        messages.success(request, 'Site atualizado com sucesso.')
        return redirect(reverse('site:edit-site', args=[url]))
    
    context = {
        'form' : form,
        'site' : site,
        'breadcrumbs': [
            {'label': 'Editar Site', 'url': None}
        ]
    }

    return render(request, 'site/edit_site.html', context)


@PermissionRoot()
def delete_site(request, url):
    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)

    if request.method == 'POST':
        site.delete()
        messages.success(request, 'Site removido do sistema.')
        return redirect('site:dashboard')
    context = {
        'site' : site
    }
    return render(request, 'site/delete_site.html', context)
