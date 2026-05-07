from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth
from django.conf import settings

from django.utils.http import url_has_allowed_host_and_scheme


from a_Account.forms import LoginForm


def login(request):

    form = LoginForm(request.POST or None)
    context = {
        'form': form
    }
    next = 'account:login'
    if form.is_valid() and request.method=='POST':
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = auth.authenticate(email=username, password=password)
        # Verifica se o usuário existe
        if user:
            # Verifica se o usuário esta ativo
            if user.is_active:
                next_url = request.GET.get('next')
                if (next_url and not next_url.startswith('//') and ':/' not in next_url and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()})):
                    final_redirect_url = next_url

                    if getattr(settings, 'USE_2FA', False):
                        # 2. Configura a sessão para o fluxo de 2FA (SEMPRE)
                        request.session['pre_2fa_user_id'] = user.id
                        request.session['next'] = final_redirect_url

                        # 3. Redireciona para a verificação de 2FA
                        return redirect('account:two_factor_verify')
                    else:
                        auth.login(request, user)
                        return redirect(final_redirect_url)
                else:
                    messages.warning(request, f'Usuário {user.first_name} esta impedido de acessar o sistema.')
            else:
                messages.warning(request, 'Usuário ou senha invalida! Corrija e tente novamente.')

    return render(request, 'account/login.html', context=context)