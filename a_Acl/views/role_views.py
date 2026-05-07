from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from a_Acl.models import FactoryClassModel
from a_Acl.forms import CreateRoleForm

from a_Site.models import FactoryClassModel as SiteFactoryClassModel

from a_Account.anotations import PermissionRoot


@PermissionRoot()
def create_role(request):
    form = CreateRoleForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Role registrado com sucesso.')
        return redirect('acl:create-role')
    context = {
        'form' : form
    }
    return render(request, 'acl/create_role.html', context)


@PermissionRoot()
def edit_role(request, rid):
    Role = FactoryClassModel.get_class('role')
    role = get_object_or_404(Role, pk=rid)

    form = CreateRoleForm(request.POST or None, instance=role)
    if form.is_valid() and request.method == 'POST':
        form.save()
        messages.success(request, 'Role atualizado com sucesso.')
        return redirect(reverse('acl:edit-role', args=[rid,]))
    context = {
        'form': form,
        'role' : role
    }
    return render(request, 'acl/edit_role.html', context)


@PermissionRoot()
def delete_role(request, rid):
    Role = FactoryClassModel.get_class('role')
    role = get_object_or_404(Role, pk=rid)

    if request.method == 'POST':
        role.delete()
        messages.success(request, 'Perfil excluído com sucesso do sistema.')
        return redirect('acl:list-roles')
    context = {
        'role' : role
    }
    return render(request, 'acl/delete_role.html', context)


@PermissionRoot()
def manage_role_permissions(request, rid):
    Role = FactoryClassModel.get_class('role')
    Permission = FactoryClassModel.get_class('permission')
    
    role = get_object_or_404(Role, pk=rid)
    
    if request.method == 'POST':
        permission_ids = request.POST.getlist('permissions')
        role.permissions.set(permission_ids)
        messages.success(request, f'Permissões do perfil "{role.nome}" atualizadas.')
        return redirect('acl:list-roles')

    # Busca todas as permissões agrupadas por ContentType para o modal
    permissions = Permission.objects.all().select_related('content_type').order_by('content_type__tipo', 'nome')
    
    assigned_permissions = role.permissions.values_list('id', flat=True)

    context = {
        'role': role,
        'permissions': permissions,
        'assigned_permissions': assigned_permissions,
    }
    return render(request, 'acl/partials/role_permissions_modal.html', context)


@PermissionRoot()
def list_roles(request):
    Role = FactoryClassModel.get_class('role')
    role_list = Role.objects.all().order_by('-level')

    search_query = request.GET.get('q')
    if search_query:
        from django.db.models import Q
        role_list = role_list.filter(
            Q(nome__icontains=search_query) | 
            Q(slug__icontains=search_query)
        )

    paginator = Paginator(role_list, 20)
    page = request.GET.get('page')
    
    try:
        roles = paginator.page(page)
    except PageNotAnInteger:
        roles = paginator.page(1)
    except EmptyPage:
        roles = paginator.page(paginator.num_pages)

    context = {
        'roles' : roles
    }

    return render(request, 'acl/list_roles.html', context)