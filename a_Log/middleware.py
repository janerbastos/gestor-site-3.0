from django.core.exceptions import PermissionDenied

from a_Log.services.security_service import (
    SecurityService
)


class PortalSecurityMiddleware:
    """
    Middleware responsável pelo monitoramento
    de eventos de segurança do portal.

    Objetivos:
    - Registrar eventos críticos
    - Capturar erros segurança
    - Monitorar acessos negados
    - Detectar possíveis ataques

    Eventos monitorados:
    - 403
    - 404
    - PermissionDenied
    - falhas críticas

    Observações:
    - NÃO registra todos os acessos
    - NÃO substitui access logs do Nginx
    - Deve permanecer leve
    """

    def __init__(self, get_response):

        self.get_response = get_response


    def __call__(self, request):
        """
        Processa request/responses.
        """

        response = self.get_response(
            request
        )

        try:

            site = getattr(
                request,
                'site',
                None
            )

            # 403
            if response.status_code == 403:

                SecurityService.register_403(

                    request=request,

                    site=site,

                    message='Acesso negado'
                )

            # 404
            elif response.status_code == 404:

                SecurityService.register_404(

                    request=request,

                    site=site,

                    message='Página não encontrada'
                )

        except Exception:

            # middleware segurança nunca deve quebrar request
            pass

        return response


    def process_exception(
        self,
        request,
        exception
    ):
        """
        Captura exceções críticas.
        """

        try:

            site = getattr(
                request,
                'site',
                None
            )

            # PermissionDenied
            if isinstance(
                exception,
                PermissionDenied
            ):

                SecurityService.register_403(

                    request=request,

                    site=site,

                    message=str(exception)
                )

        except Exception:

            pass

        return None