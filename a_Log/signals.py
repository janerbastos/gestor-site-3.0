from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed
)

from django.dispatch import receiver

from a_Log.services.audit_service import (
    AuditService
)

from a_Log.services.security_service import (
    SecurityService
)


"""
Signals responsáveis pelo monitoramento de autenticação
e eventos globais do sistema.

Objetivos:
- registrar login/logout
- registrar falhas autenticação
- alimentar auditoria
- alimentar segurança

Observações:
- signals devem permanecer leves
- evitar lógica pesada
- evitar consultas complexas
- ideal integrar com Celery futuramente
"""


@receiver(user_logged_in)
def register_user_login(sender, request, user, **kwargs):
    """
    Registra autenticação realizada.
    """
    try:
        site = getattr(request, 'site', None)
        AuditService.register_login(request=request, site=site, user=user, message='Usuário autenticado')
    except Exception as e:
        print(e)


@receiver(user_logged_out)
def register_user_logout(sender, request, user, **kwargs):
    """
    Registra logout do usuário.
    """
    try:
        site = getattr(request, 'site', None)
        AuditService.register_logout(request=request, site=site, user=user, message='Usuário desconectado')
    except Exception:
        pass


@receiver(user_login_failed)
def register_user_login_failed(sender, credentials, request, **kwargs):
    """
    Registra falhas autenticação.
    """
    try:
        site = getattr(request, 'site', None) if request else None
        SecurityService.register_login_fail(request=request, site=site, message='Falha autenticação')
    except Exception:
        pass