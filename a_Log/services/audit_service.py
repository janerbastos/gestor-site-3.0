from django.utils import timezone

from a_Log.models.audit import AuditLog


class AuditService:
    """
    Serviço responsável pelo registro de eventos de auditoria.

    Objetivos:
    - Centralizar criação de logs administrativos
    - Padronizar auditoria do CMS
    - Evitar duplicação de lógica nas views
    - Facilitar integração futura com filas e observabilidade

    Exemplos:
    - criação conteúdo
    - atualização
    - exclusão
    - login/logout
    - publicação
    - alteração permissões
    """

    @classmethod
    def register(cls, request, site, action, obj=None, message='', metadata=None):
        """
        Registra evento de auditoria.
        Args:
            request:
                HttpRequest atual.
            site:
                Instância do portal/site.
            action:
                Tipo da ação executada.
            obj:
                Objeto relacionado ao evento.
            message:
                Descrição amigável do evento.
            metadata:
                Informações adicionais serializáveis.
        """

        AuditLog.objects.create(
            site=site,
            user=(request.user if request.user.is_authenticated else None ),
            action=action,
            object_type=(obj.__class__.__name__ if obj else ''),
            object_id=(obj.id if obj else None),
            message=message, ip=cls.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            path=request.path,
            metadata=metadata or {},
            create_at=timezone.now()
        )


    @classmethod
    def register_create(cls, request, site, obj, message='Registro criado', metadata=None):

        cls.register(
            request=request,
            site=site,
            action=AuditLog.ACTION_CREATE,
            obj=obj,
            message=message,
            metadata=metadata
        )


    @classmethod
    def register_update(cls, request, site, obj, message='Registro atualizado',metadata=None):

        cls.register(
            request=request,
            site=site,
            action=AuditLog.ACTION_UPDATE,
            obj=obj,
            message=message,
            metadata=metadata
        )


    @classmethod
    def register_delete(cls, request, site, obj, message='Registro removido',metadata=None):

        cls.register(
            request=request,
            site=site,
            action=AuditLog.ACTION_DELETE,
            obj=obj,
            message=message,
            metadata=metadata
        )


    @classmethod
    def register_login(cls, request, site, user, message='Usuário autenticado'):

        AuditLog.objects.create(
            site=site,
            user=user,
            action=AuditLog.ACTION_LOGIN,
            object_type='User',
            object_id=user.id,
            message=message,
            ip=cls.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            path=request.path
        )


    @classmethod
    def register_logout(cls, request, site, user, message='Usuário desconectado'):

        AuditLog.objects.create(
            site=site,
            user=user,
            action=AuditLog.ACTION_LOGOUT,
            object_type='User',
            object_id=user.id,
            message=message,
            ip=cls.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            path=request.path
        )


    @staticmethod
    def get_client_ip(request):
        """
        Obtém IP real do cliente.
        Compatível com proxy reverso.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')