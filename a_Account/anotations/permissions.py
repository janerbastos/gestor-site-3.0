from functools import wraps
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages


class PermissionRoot(object):
    def __init__(self, login_url='account:login'):
        self.login_url = login_url

    def __call__(self, f):
        @wraps(f)
        def wrapped_f(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated and user.is_superuser:
                return f(request, *args, **kwargs)
            messages.warning(request, 'Usuário não possui autorização para acessar esse conteúdo.')
            return redirect_to_login(
                next=request.get_full_path(),
                login_url=self.login_url
            )
        return wrapped_f