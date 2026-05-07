from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from a_Site.models import FactoryClassModel
from a_Acl.models import FactoryClassModel as FactoryClassModelRole
from a_Acl.forms import CreateSiteUserForm, EditSiteUserRolesForm
from a_Account.anotations import PermissionRoot



@PermissionRoot()
def manage_user_roles(request, url, member_id):
    Site = FactoryClassModel.get_class('site')
    SiteRole = FactoryClassModelRole.get_class('site_role')
    site = get_object_or_404(Site, url=url)
    member = get_object_or_404(SiteRole, id=member_id, site=site)

    form = EditSiteUserRolesForm(request.POST or None, instance=member)

    if form.is_valid() and request.method == 'POST':
        form.save()
        
        if request.headers.get('HX-Request'):
            # Retorna apenas a linha da tabela atualizada para refletir os novos papéis
            context = {'member': member, 'site': site}
            return render(request, 'acl/partials/user_table_row.html', context)
        
        messages.success(request, f"Papéis de {member.user.get_full_name} atualizados.")
        return redirect(reverse('acl:list-users', args=[url]))

    context = {
        'site': site,
        'member': member,
        'form': form,
    }

    return render(request, 'acl/partials/manage_user_roles_modal.html', context)


@PermissionRoot()
def manage_site_user(request, url):
     Site = FactoryClassModel.get_class('site')
     SiteRole = FactoryClassModelRole.get_class('site_role')
     site = get_object_or_404(Site, url=url)

     # Lógica de adição de usuário ao site
     if request.method == 'POST' and request.POST.get('action') == 'add_user':
         user_id = request.POST.get('user_id')
         if user_id:
             from a_Account.models import User
             user = get_object_or_404(User, id=user_id)

             # Tenta criar a autorização inicial (SiteRole)
             obj, created = SiteRole.objects.get_or_create(site=site, user=user)

             if request.headers.get('HX-Request'):
                 from django.http import HttpResponse
                 msg = f"Usuário {user.get_full_name} adicionado." if created else f"{user.get_full_name} já possui acesso."
                 icon = "fa-check-circle text-green-500" if created else "fa-info-circle text-blue-500"
                 bg = "bg-green-50/50" if created else "bg-blue-50/50"
                 text = "text-green-700" if created else "text-blue-700"
                 border = "border-green-100" if created else "border-blue-100"

                 html = f"""
                 <div class="flex items-center justify-center p-6 {bg} transition-all animate-fade-in-up border-b border-slate-50 dark:border-gray-800 h-[88px]">
                     <div class="flex items-center gap-3 {text} px-6 py-2.5 bg-white dark:bg-gray-900 rounded-2xl shadow-sm border {border} dark:border-gray-700">
                         <i class="fas {icon} text-sm"></i>
                         <span class="text-xs font-black uppercase tracking-widest">{msg}</span>
                     </div>
                 </div>
                 """
                 return HttpResponse(html)
             if created:
                 messages.success(request, f"Usuário {user.get_full_name} adicionado ao site.")

             return redirect(reverse('acl:list-users', args=[url]))         
     # Lógica de busca de usuários globais (que não estão no site)
     search_query = request.GET.get('q')
     users_found = []
     if search_query:
         from a_Account.models import User
         from django.db.models import Q
         
         # Busca usuários que contenham o termo no nome ou email
         # Exclui os que já estão no site
         membros_ids = site.membros_roles.values_list('user_id', flat=True)
         users_found = User.objects.filter(
             Q(first_name__icontains=search_query) | 
             Q(last_name__icontains=search_query) |
             Q(email__icontains=search_query)
         ).exclude(id__in=membros_ids)[:10]
 
     context = {
         'site': site,
         'users_found': users_found,
         'search_query': search_query,
     }
 
     if request.headers.get('HX-Request'):
         # Se for uma busca dinâmica disparada pelo input
         if request.headers.get('HX-Target') == 'search-results-container':
             return render(request, 'acl/partials/user_search_results.html', context)
         # Se for o carregamento inicial do modal no clique do botão
         return render(request, 'acl/partials/user_permissions_modal.html', context)

     # Caso acesso direto (não-HTMX), redireciona para a listagem
     return redirect(reverse('acl:list-users', args=[url]))



@PermissionRoot()
def list_users(request, url):
    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)

    user_list = site.membros_roles.all()

    search_query = request.GET.get('q')
    if search_query:
        from django.db.models import Q
        user_list = user_list.filter(
            Q(user__first_name__icontains=search_query) | 
            Q(user__last_name__icontains=search_query)
        )

    paginator = Paginator(user_list, 20)
    page = request.GET.get('page')
    
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context = {
        'site': site,
        'users' : users,
        'breadcrumbs': [
            {'label': 'Equipe e Permissões', 'url': None}
        ]
    }

    return render(request, 'acl/list_user_site.html', context)


@PermissionRoot()
def remove_user_site(request, url, oid):
    Site = FactoryClassModel.get_class('site')
    site = get_object_or_404(Site, url=url)
    autorizacao = get_object_or_404(site.membros_roles, pk=oid)

    if request.method == 'POST':
        
        autorizacao.delete()
        messages.success(request, 'Usuário retirado do site')
        return redirect(reverse('acl:list-users', args=(url,)))
    
    context = {
        'site' : site,
        'autorizacao' : autorizacao
    }

    return render(request, 'acl/delete_user_site.html', context)
    