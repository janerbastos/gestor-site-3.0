from functools import wraps
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from functools import wraps

from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


class PermissionRoot:

    def __init__(self, login_url='account:login'):

        self.login_url = login_url


    def __call__(self, f):

        @wraps(f)
        def wrapped_f(request, *args, **kwargs):

            user = request.user

            # não autenticado
            if not user.is_authenticated:
                messages.warning(
                    request,
                    'Realize login para acessar o conteúdo.'
                )
                return redirect_to_login(
                    next=request.get_full_path(),
                    login_url=self.login_url
                )

            # autenticado mas sem permissão
            if not user.is_superuser:

                raise PermissionDenied(
                    'Usuário não possui autorização.'
                )

            return f(request, *args, **kwargs)

        return wrapped_f