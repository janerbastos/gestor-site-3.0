from django.shortcuts import render, get_object_or_404

from a_Site.models import FactoryClassModel
from a_Account.anotations import PermissionRoot
from a_Content.models import Content
from a_Content.services.core.dispatcher import ServiceDispatcher


@PermissionRoot()
def dashboard(request, url, path_url=None):
    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)
    
    parent = None # Representa a rais do site
    breadcrumbs = []

    # Busca o conteúdo base (raiz ou pasta específica)
    if path_url:
        if not path_url.endswith('/'):
            path_url += '/'
        parent = get_object_or_404(Content, path=path_url, site=site)
        # Gera os breadcrumbs percorrendo os pais
        curr = parent
        while curr:
            breadcrumbs.insert(0, curr)
            curr = curr.parent
    
    # Inicializa as variaveis de sessão

    if request.method == 'POST':

        action = request.POST.get('action')
        type_ = request.POST.get('content')
        content_id = request.POST.get('content_id')

        if action and type_:
            # Descoberta de view de serviço
            return ServiceDispatcher.dispatch(
            'Service',
            'view',
            data={'action': action, 'type': type_, 'parent': parent, 'request': request, 'url': url, 'content_id': content_id}
        )

    # Filtra conteúdos: se tiver pai, pega os filhos. Se não, pega a raiz.
    catalogs = site.catalogs.filter(parent=parent)
    
    # Busca simplificada se houver termo
    search_query = request.GET.get('q')
    if search_query:
        catalogs = catalogs.filter(titulo__icontains=search_query)

    context = {
        'site': site,
        'catalogs': catalogs,
        'parent': parent,
        'breadcrumbs': breadcrumbs,
        'search_query': search_query,
        'content_types' : site.tipos_conteudo.all(),
        'dashboards': {'label': 'Gestor de Conteúdo', 'url': None}
    }

    return render(request, 'content/dashboard.html', context)


@PermissionRoot()
def manage_content(request, url):

    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)

    parent=None
    type_ = request.session.get('type')
    action = request.session.get('action')
    parent_id = request.session.get('parent_id')

    if parent_id:
        parent = get_object_or_404(Content, parent__id=parent_id, site=site)

    result = ServiceDispatcher.dispatch(
        type_,
        action,
        data=request.POST
    )


    return render(request, 'content/manager_content.html', {'result': result})



    