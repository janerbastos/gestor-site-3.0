from django.utils import timezone

from a_Log.models.security import SecurityLog


class SecurityService:
    """
    Serviço responsável pelo registro de eventos de segurança.

    Objetivos:
    - Centralizar logs de segurança
    - Registrar acessos suspeitos
    - Detectar falhas autenticação
    - Monitorar eventos críticos
    - Facilitar integração com observabilidade

    Eventos suportados:
    - login_fail
    - 403
    - 404
    - bruteforce
    - blocked
    - suspicious
    - invalid_csrf
    """

    BOT_IDENTIFIERS = [
        'bot',
        'crawler',
        'spider',
        'crawl',
        'googlebot',
        'bingbot',
        'slurp',
        'duckduckbot'
    ]


    @classmethod
    def register(
        cls,
        request,
        event,
        site=None,
        severity='medium',
        message='',
        metadata=None
    ):
        """
        Registra evento de segurança.
        """

        SecurityLog.objects.create(
            site=site,
            user=(
                request.user
                if (
                    hasattr(request, 'user')
                    and request.user.is_authenticated
                )
                else None
            ),
            event=event,
            severity=severity,
            ip=cls.get_client_ip(
                request
            ),
            path=request.path,
            method=request.method,
            user_agent=request.META.get(
                'HTTP_USER_AGENT',
                ''
            ),
            referer=request.META.get(
                'HTTP_REFERER',
                ''
            ),
            message=message,
            metadata=metadata or {},
            is_bot=cls.is_bot(
                request
            ),
            create_at=timezone.now()
        )


    @classmethod
    def register_403(
        cls,
        request,
        site=None,
        message='Acesso negado'
    ):
        cls.register(
            request=request,
            site=site,
            event=SecurityLog.EVENT_403,
            severity='medium',
            message=message
        )


    @classmethod
    def register_404(
        cls,
        request,
        site=None,
        message='Recurso não encontrado'
    ):

        cls.register(
            request=request,
            site=site,
            event=SecurityLog.EVENT_404,
            severity='low',
            message=message
        )


    @classmethod
    def register_login_fail(
        cls,
        request,
        site=None,
        message='Falha autenticação'
    ):

        cls.register(
            request=request,
            site=site,
            event=SecurityLog.EVENT_LOGIN_FAIL,
            severity='high',
            message=message
        )


    @classmethod
    def register_bruteforce(
        cls,
        request,
        site=None,
        message='Tentativa brute force detectada'
    ):

        cls.register(
            request=request,
            site=site,
            event=SecurityLog.EVENT_BRUTEFORCE,
            severity='critical',
            message=message
        )


    @classmethod
    def register_blocked(
        cls,
        request,
        site=None,
        message='Acesso bloqueado'
    ):

        cls.register(
            request=request,
            site=site,
            event=SecurityLog.EVENT_BLOCKED,
            severity='high',
            message=message
        )


    @classmethod
    def register_invalid_csrf(
        cls,
        request,
        site=None,
        message='Falha validação CSRF'
    ):

        cls.register(
            request=request,
            site=site,
            event=SecurityLog.EVENT_INVALID_CSRF,
            severity='high',
            message=message
        )


    @classmethod
    def register_suspicious(
        cls,
        request,
        site=None,
        message='Atividade suspeita detectada',
        metadata=None
    ):

        cls.register(
            request=request,
            site=site,
            event=SecurityLog.EVENT_SUSPICIOUS,
            severity='critical',
            message=message,
            metadata=metadata
        )


    @classmethod
    def is_bot(cls, request):
        """
        Detecta bots simples via User-Agent.
        """

        user_agent = request.META.get(
            'HTTP_USER_AGENT',
            ''
        ).lower()

        return any(
            identifier in user_agent
            for identifier in cls.BOT_IDENTIFIERS
        )


    @staticmethod
    def get_client_ip(request):
        """
        Obtém IP real do cliente.
        """

        x_forwarded_for = request.META.get(
            'HTTP_X_FORWARDED_FOR'
        )

        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()

        return request.META.get(
            'REMOTE_ADDR'
        )