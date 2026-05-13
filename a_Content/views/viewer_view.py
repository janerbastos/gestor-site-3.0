from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.utils.dateparse import parse_datetime

from a_Site.models import FactoryClassModel
from a_Content.models import Content
from a_Content.forms.viewer_forms import FactoryATViewerForm
from a_Content.services.core.dispatcher import ServiceDispatcher
from a_Content.services.comum_service import BaseContentServiceLog

from a_Acl.anotations import PermissionRequired


# limpar session

def clear_session(request):
    for key in ['type', 'action', 'content_id']:
        request.session.pop(key, None)


@PermissionRequired('create', 'ATView')
def create_viewer(request, url):

    Site = FactoryClassModel.get_class('site')
    ContentType = FactoryClassModel.get_class('tipo')
    site = get_object_or_404(Site, url=url)
    service_log = BaseContentServiceLog(request, site)

    type_ = request.session.get('type')
    action = request.session.get('action')
    parent_id = request.session.get('parent_id')

    if not all([type_, action]):
        messages.error(request, 'Sessão inválida.')
        return redirect(reverse('content:dashboard', args=[url]))

    parent = None

    if parent_id:
        parent = get_object_or_404(
            Content,
            id=parent_id,
            site=site
        )

    CreateForm = FactoryATViewerForm.get_class('create')

    if request.method == 'POST':

        form = CreateForm(request.POST, request.FILES)

        if form.is_valid():
            user = request.user
            data = form.cleaned_data
            data['dono_id'] = user.id
            data['parent_id'] = parent_id
            data['site_id'] = site.id
            data['tipo'] = ContentType.ATVIEWER
            result, message, obj = ServiceDispatcher.dispatch(
                type_,
                action,
                data=data,
            )
            clear_session(request)
            args = [url]
            if result == 'success':
                service_log.log_create(obj) # Registra no serviço de log
                if parent:
                    args.append(obj.parent.path)
                messages.success(request, message)
            else:
                messages.error(request, message)

            return redirect(
                reverse('content:dashboard', args=args)
            )

    else:

        form = CreateForm()

    context = {
        'site': site,
        'form': form,
        'parent': parent
    }

    return render(
        request,
        f'content/{type_.lower()}-{action}.html',
        context
    )


@PermissionRequired('update', 'ATView')
def update_viewer(request, url):

    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)
    service_log = BaseContentServiceLog(request, site)

    type_ = request.session.get('type')
    action = request.session.get('action')
    content_id = request.session.get('content_id')

    if not all([type_, action, content_id]):
        messages.error(request, 'Sessão inválida.')
        return redirect(reverse('content:dashboard', args=[url]))

    content = get_object_or_404(
        Content,
        id=content_id,
        site=site
    )

    parent = content.parent

    CreateForm = FactoryATViewerForm.get_class('create')

    if request.method == 'POST':
        form = CreateForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            data['id'] = content.id
            result, message, obj = ServiceDispatcher.dispatch(
                type_,
                action,
                data=data
            )
            clear_session(request)
            args = [url]
            if result == 'success':
                service_log.log_update(obj, content) # registra no serviço de log
                if parent:
                    args.append(parent.path)
                messages.success(request, message)
            else:
                messages.error(request, message)
            return redirect(
                reverse('content:dashboard', args=args)
            )
    else:
        viewer_data = content.data or {}

        form = CreateForm(initial={
            'titulo': content.titulo,
            'url': content.url,
            'descricao': content.descricao,
            'corpo': content.corpo,
            'tag': content.tag,

            'show_in_menu': content.show_in_menu,
            'excluir_nav': content.excluir_nav,

            'viewer_mode': viewer_data.get('viewer_mode'),
            'target_path': viewer_data.get('target_path'),
            'template_name': viewer_data.get('template_name'),
            'ordering': viewer_data.get('ordering'),
            'limit': viewer_data.get('limit'),
        })



    context = {
        'site': site,
        'form': form,
        'parent': parent,
        'content': content
    }

    return render(
        request,
        f'content/{type_.lower()}-{action}.html',
        context
    )


@PermissionRequired('delete', 'ATView')
def delete_viewer(request, url):

    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)
    service_log = BaseContentServiceLog(request, site)

    type_ = request.session.get('type')
    action = request.session.get('action')
    content_id = request.session.get('content_id')

    content = get_object_or_404(Content, id=content_id)
    parent = content.parent

    if request.method == 'POST':

        result, message = ServiceDispatcher.dispatch(
            type_,
            action,
            data={'content_id':content_id}
        )

        # Limpar session
        clear_session(request)

        args = [url]
        if result == 'success':
            service_log.log_delete(content) # registra no serviço de log
            if parent:
                args.append(parent.path)

            messages.success(request, message)
        else:
            messages.error(request, message)
        return redirect(reverse('content:dashboard', args=args))


    context = {
        'site' : site,
        'parent': parent,
        'content': content
    }

    return render(request, f'content/{type_.lower()}-{action}.html', context)


@PermissionRequired('workflow', 'ATView')
def workflow_viewer(request, url):

    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)
    service_log = BaseContentServiceLog(request, site)

    type_ = request.session.get('type')
    action = request.session.get('action')
    content_id = request.session.get('content_id')

    if not all([type_, action, content_id]):
        return HttpResponse('Sessão inválida.', status=400)

    content = get_object_or_404(
        Content,
        id=content_id,
        site=site
    )

    parent = content.parent

    if request.method == 'POST':
        workflow = request.POST.get('workflow')
        if workflow:
            result, message, obj = ServiceDispatcher.dispatch(
                type_,
                action,
                data={
                    'content_id': content_id,
                    'workflow': workflow
                }
            )

            service_log.log_update(content, obj) # registra no serviço de log

            # Atualizar objeto após alteração
            content.refresh_from_db()

            context = {
                'site': site,
                'parent': parent,
                'content': content,
                'message': message,
                'result': result
            }

            return render(
                request,
                'content/partials/content-table-row.html',
                context
            )

    context = {
        'site': site,
        'parent': parent,
        'content': content
    }

    return render(
        request,
        f'content/{type_.lower()}-{action}.html',
        context
    )