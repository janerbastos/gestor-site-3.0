from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth, messages
from django.conf import settings
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from a_Account.forms import CreateUserForm
from a_Account.services import AccountService
from a_Account.anotations import PermissionRoot


@PermissionRoot()
def list_users(request):
    User = auth.get_user_model()
    user_list = User.objects.all().order_by('-date_joined')

    search_query = request.GET.get('q')
    if search_query:
        from django.db.models import Q
        user_list = user_list.filter(
            Q(first_name__icontains=search_query) | 
            Q(last_name__icontains=search_query) | 
            Q(email__icontains=search_query)
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
        'users' : users
    }

    return render(request, 'account/list_users.html', context)

@PermissionRoot()
def create_user(request):
    form = CreateUserForm(request.POST or None)
    context = {
        'form' : form
    }
    if form.is_valid() and request.method == 'POST':
        user = form.save()
        messages.success(request, 'Usuário registrado com sucesso.')
        result, message = AccountService.notification_create_user(request, user)
        
        if result == 'success':
            messages.success(request, message)
            return redirect('account:create-user')
        else:
            messages.error(request, message)
    
    return render(request, 'account/create_user_form.html', context=context)


@PermissionRoot()
def edit_user(request, uid):
    User = auth.get_user_model()
    user = get_object_or_404(User, pk=uid)
    form = CreateUserForm(request.POST or None, instance=user)
    if form.is_valid() and request.method == 'POST':
        form.save()
        messages.success(request, 'Usuário registrado com sucesso.')
        return redirect(reverse('account:edit-user', args=[uid,]))
    context = {
        'form' : form
    }

    return render(request, 'account/edit_user_form.html', context)


@PermissionRoot()
def delete_user(request, uid):
    User = auth.get_user_model()
    user = get_object_or_404(User, pk=uid)
    if request.method == 'POST':
        user.delete()
        return redirect('account:create-user')
    context = {
        'user' : user
    }
    return render(request, 'account/delete_user_form.html', context)