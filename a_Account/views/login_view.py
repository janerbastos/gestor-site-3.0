from django.conf import settings
from django.contrib import auth
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.http import (
    url_has_allowed_host_and_scheme
)

from a_Account.forms import LoginForm


def login(request):

    form = LoginForm(request.POST or None)

    context = {'form': form}

    if (request.method == 'POST' and form.is_valid()):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = auth.authenticate(
            request,
            email=username,
            password=password
        )

        # usuário inválido
        if user is None:
            messages.error(request, 'Usuário ou senha inválidos.')
            return render(request, 'account/login.html', context)

        # usuário inativo
        if not user.is_active:

            messages.error(request, f'Usuário {user.first_name} está desativado.')
            return render(request, 'account/login.html', context)

        # next
        next_url = request.GET.get('next')

        # valida URL
        if (next_url and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()})):
            final_redirect_url = next_url
        else:
            final_redirect_url = '/'

        # 2FA
        if getattr(settings, 'USE_2FA', False):
            request.session['pre_2fa_user_id'] = user.id
            request.session['next'] = final_redirect_url
            return redirect('account:two_factor_verify')

        # login normal
        auth.login(request, user)

        return redirect(final_redirect_url)

    return render(request, 'account/login.html', context)


def logout(request):
    """
    Encerra sessão autenticada do usuário.
    """

    if request.user.is_authenticated:

        auth.logout(request)

        messages.success(
            request,
            'Sessão encerrada com sucesso.'
        )

    return redirect('account:login')