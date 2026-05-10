from functools import wraps

from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages

from a_Acl.services import ACLService


class PermissionRequired:

    def __init__(
        self,
        permission_slug,
        tipo,
        login_url='account:login'
    ):

        self.permission_slug = permission_slug
        self.tipo = tipo
        self.login_url = login_url


    def __call__(self, f):

        @wraps(f)
        def wrapped_f(request, *args, **kwargs):

            user = request.user

            # login obrigatório
            if not user.is_authenticated:

                messages.warning(
                    request,
                    'Realize login para acessar o conteúdo.'
                )

                return redirect_to_login(
                    next=request.get_full_path(),
                    login_url=self.login_url
                )

            # superusuário
            if user.is_superuser:
                return f(request, *args, **kwargs)

            site = kwargs.get('url')

            has_permission = ACLService.has_permission(
                user,
                site,
                self.tipo,
                self.permission_slug
            )

            # sem permissão
            if not has_permission:

                raise PermissionDenied(
                    'Usuário não possui autorização.'
                )

            return f(request, *args, **kwargs)

        return wrapped_f