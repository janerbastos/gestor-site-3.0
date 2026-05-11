from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    """
    Modelos de auditoria do CMS.

    Este módulo é responsável por registrar eventos administrativos
    e ações críticas executadas dentro do sistema, permitindo
    rastreabilidade, conformidade e histórico operacional.

    Objetivos:
    - Registrar ações administrativas
    - Permitir rastreamento de alterações
    - Apoiar auditoria e compliance
    - Identificar responsáveis por operações
    - Gerar histórico de atividades do portal

    Eventos suportados:
    - create      → criação de registros
    - update      → atualização de registros
    - delete      → remoção de registros
    - login       → autenticação de usuário
    - logout      → encerramento de sessão
    - publish     → publicação de conteúdo
    - permission  → alteração de permissões

    Exemplos de uso:
    - Auditoria de conteúdos
    - Histórico de alterações
    - Rastreio de permissões
    - Controle administrativo
    - Investigações operacionais

    Arquitetura:
    Os registros devem ser criados preferencialmente por:
    - services/audit_service.py
    - signals Django
    - decorators
    - middlewares específicos

    Boas práticas:
    - NÃO registrar pageviews públicos
    - NÃO armazenar uploads binários
    - Evitar payloads excessivos em metadata
    - Priorizar eventos relevantes

    Observações:
    - O campo metadata permite extensibilidade
    - Os índices foram adicionados para otimizar consultas
    - Ideal para dashboards administrativos e compliance

    Autor: Janer
    """

    ACTION_CREATE = 'create'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'
    ACTION_LOGIN = 'login'
    ACTION_LOGOUT = 'logout'
    ACTION_PUBLISH = 'publish'
    ACTION_PERMISSION = 'permission'

    CHOICES_ACTION = (
        (ACTION_CREATE, 'Criação'),
        (ACTION_UPDATE, 'Atualização'),
        (ACTION_DELETE, 'Exclusão'),
        (ACTION_LOGIN, 'Login'),
        (ACTION_LOGOUT, 'Logout'),
        (ACTION_PUBLISH, 'Publicação'),
        (ACTION_PERMISSION, 'Permissão'),
    )
    site = models.ForeignKey(
        'a_Site.Site',
        on_delete=models.CASCADE,
        related_name='audit_logs',
        null=True, blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    action = models.CharField(
        max_length=30,
        choices=CHOICES_ACTION
    )
    object_type = models.CharField(
        max_length=100,
        help_text='Nome do model afetado'
    )
    object_id = models.PositiveBigIntegerField(
        null=True,
        blank=True
    )
    message = models.TextField(
        blank=True,
        null=True
    )
    ip = models.GenericIPAddressField(
        null=True,
        blank=True
    )
    user_agent = models.TextField(
        blank=True,
        null=True
    )
    path = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )
    metadata = models.JSONField(
        default=dict,
        blank=True
    )
    create_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        db_table = 'a_log_audit'
        verbose_name = 'Log de Auditoria'
        verbose_name_plural = 'Logs de Auditoria'
        ordering = ['-create_at']
        indexes = [
            models.Index(
                fields=['site']
            ),
            models.Index(
                fields=['user']
            ),
            models.Index(
                fields=['action']
            ),
            models.Index(
                fields=['create_at']
            ),
        ]

    def __str__(self):

        return (
            f'{self.user} - '
            f'{self.action} - '
            f'{self.object_type}'
        )

    def json(self):

        return {
            'id': self.id,
            'site': self.site_id,
            'user': (
                self.user.username
                if self.user
                else None
            ),
            'action': self.action,
            'object_type': self.object_type,
            'object_id': self.object_id,
            'message': self.message,
            'ip': self.ip,
            'path': self.path,
            'metadata': self.metadata,
            'create_at': self.create_at.isoformat()
        }