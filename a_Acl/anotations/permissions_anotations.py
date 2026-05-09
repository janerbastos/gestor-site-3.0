from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login

from a_Acl.services import ACLService


from functools import wraps
from django.core.exceptions import PermissionDenied


class PermissionRequired:

    def __init__(self, permission_slug, tipo):

        self.permission_slug = permission_slug
        self.tipo = tipo


    def __call__(self, f):

        @wraps(f)
        def wrapped_f(request, *args, **kwargs):

            user = request.user

            # superusuário
            if user.is_superuser:
                return f(request, *args, **kwargs)

            site = kwargs.get('url')

            print('USER:', user)
            print('SITE:', site)
            print('TIPO:', self.tipo)
            print('PERMISSION:', self.permission_slug)

            has_permission = ACLService.has_permission(
                user,
                site,
                self.tipo,
                self.permission_slug
            )

            if not has_permission:
                raise PermissionDenied()

            return f(request, *args, **kwargs)

        return wrapped_f
