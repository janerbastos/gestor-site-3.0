from django.shortcuts import (
    render, redirect, get_object_or_404
    )
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import (
    Paginator, EmptyPage, PageNotAnInteger
    )
from django.db.models import Q

from a_Site.models import FactoryClassModel
from a_Site.forms import CreateSiteForm
from a_Account.anotations import PermissionRoot



@PermissionRoot()
def dashboard(request):
    """
    Dashboard principal de gerenciamento de sites.
    Responsável por:
        - listar sites cadastrados;
        - aplicar busca textual;
        - paginar resultados.
    """

    Site = FactoryClassModel.get_class('site')

    site_list = (
        Site.objects
        .all()
        .order_by('titulo')
    )

    # Busca textual
    search_query = request.GET.get('q', '').strip()

    if search_query:
        site_list = site_list.filter(
            Q(titulo__icontains=search_query) |
            Q(descricao__icontains=search_query) |
            Q(url__icontains=search_query)
        )

    # Paginação
    paginator = Paginator(site_list, 20)
    page = request.GET.get('page', 1)

    try:
        sites = paginator.page(page)

    except PageNotAnInteger:
        sites = paginator.page(1)

    except EmptyPage:
        sites = paginator.page(paginator.num_pages)

    context = {
        'sites': sites,
        'search_query': search_query,
        'breadcrumbs': [],
    }

    return render(
        request,
        'site/dashboard.html',
        context
    )


@PermissionRoot()
def create_site(request):
    """
    View responsável pelo cadastro de novos sites.
    """

    form = CreateSiteForm(
        request.POST or None
    )

    if request.method == 'POST':

        if form.is_valid():

            site = form.save(commit=False)

            # Define o usuário responsável pelo site
            site.dono = request.user

            site.save()

            messages.success(
                request,
                'Site registrado com sucesso.'
            )

            return redirect('site:dashboard')

        messages.error(
            request,
            'Não foi possível registrar o site. Verifique os campos informados.'
        )

    context = {
        'form': form,
        'breadcrumbs': [
            {
                'label': 'Novo Site',
                'url': None
            }
        ]
    }

    return render(
        request,
        'site/create_site.html',
        context
    )


@PermissionRoot()
def open_site(request, url):
    """
    View responsável pela visualização
    detalhada de um site.
    """

    Site = FactoryClassModel.get_class('site')

    site = get_object_or_404(
        Site,
        url=url
    )

    context = {
        'site': site,
        'breadcrumbs': [
            {
                'label': site.titulo,
                'url': None
            }
        ]
    }

    return render(
        request,
        'site/open_site.html',
        context
    )


@PermissionRoot()
def edit_site(request, url):
    """
    View responsável pela edição
    de um site existente.
    """

    Site = FactoryClassModel.get_class('site')

    site = get_object_or_404(
        Site,
        url=url
    )

    form = CreateSiteForm(
        request.POST or None,
        instance=site
    )

    if request.method == 'POST':

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Site atualizado com sucesso.'
            )

            return redirect(
                reverse(
                    'site:edit-site',
                    args=[site.url]
                )
            )

        messages.error(
            request,
            'Não foi possível atualizar o site. Verifique os campos informados.'
        )

    context = {
        'form': form,
        'site': site,
        'breadcrumbs': [
            {
                'label': 'Editar Site',
                'url': None
            }
        ]
    }

    return render(
        request,
        'site/edit_site.html',
        context
    )


@PermissionRoot()
def delete_site(request, url):
    """
    View responsável pela remoção
    de um site do sistema.
    """

    Site = FactoryClassModel.get_class('site')

    site = get_object_or_404(
        Site,
        url=url
    )

    if request.method == 'POST':

        site.delete()

        messages.success(
            request,
            'Site removido do sistema.'
        )

        return redirect('site:dashboard')

    context = {
        'site': site,
        'breadcrumbs': [
            {
                'label': 'Remover Site',
                'url': None
            }
        ]
    }

    return render(
        request,
        'site/delete_site.html',
        context
    )
