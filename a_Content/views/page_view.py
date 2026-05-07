from django.shortcuts import render, get_object_or_404

from a_Site.models import FactoryClassModel
from a_Account.anotations import PermissionRoot
from a_Content.models import Content
from a_Content.forms.pagina_forms import FactoryATPageForm
from a_Content.services.core.dispatcher import ServiceDispatcher



def create_pagina(request, url):
    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)

    parent=None
    type_ = request.session.get('type')
    action = request.session.get('action')
    parent_id = request.session.get('parent_id')

    if parent_id:
        parent = get_object_or_404(Content, id=parent_id, site=site)
    
    CreateForm = FactoryATPageForm.get_class('create')
    form = CreateForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        ContentType = FactoryClassModel.get_class('tipo')
        user = request.user
        data = form.cleaned_data
        data['dono_id'] = user.id
        data['parent_id'] = parent_id
        data['site_id'] = site.id
        data['tipo'] = ContentType.ATPAGINA

        message, pagina = ServiceDispatcher.dispatch(
            type_,
            action,
            data=data
        )
        # Limoar cache
        print(message, pagina)
    
    context = {
        'site' : site,
        'form' : form,
        'parent': parent
    }


    return render(request, f'content/{type_.lower()}-{action}.html', context)


def update_pagina(request, url):
    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)

    parent=None
    type_ = request.session.get('type')
    action = request.session.get('action')
    content_id = request.session.get('content_id')
    parent_id = request.session.get('parent_id')

    # if parent_id:
    #     parent = get_object_or_404(Content, id=parent_id, site=site)
    content = get_object_or_404(Content, id=content_id)
    
    CreateForm = FactoryATPageForm.get_class('create')
    if request.method == 'POST':
        form = CreateForm(request.POST or None)
    else:
        form = CreateForm(initial={
                          'titulo': content.titulo, 
                          'url': content.url, 
                          'descricao': content.descricao, 
                          'corpo': content.corpo, 
                          'show_in_menu': content.show_in_menu,
                          'excluir_nav': content.excluir_nav})

    if form.is_valid() and request.method == 'POST':

        data = form.cleaned_data
        data['id'] = content.id


        message, pagina = ServiceDispatcher.dispatch(
            type_,
            action,
            data=data
        )
        # Limoar cache
        print(message, pagina)
    
    context = {
        'site' : site,
        'form' : form,
        'parent': parent,
        'content': content
    }


    return render(request, f'content/{type_.lower()}-{action}.html', context)