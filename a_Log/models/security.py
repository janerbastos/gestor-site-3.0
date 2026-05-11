from django.conf import settings
from django.db import models


class SecurityLog(models.Model):

    """
    Modelos de segurança e monitoramento do CMS.

    Este módulo é responsável por registrar eventos relacionados
    à segurança da aplicação, permitindo detecção de atividades
    suspeitas, rastreamento de acessos indevidos e auditoria
    de incidentes.

    Objetivos:
    - Monitorar eventos de segurança
    - Detectar acessos suspeitos
    - Registrar falhas de autenticação
    - Identificar tentativas de ataque
    - Auxiliar processos de investigação
    - Apoiar estratégias de proteção e bloqueio

    Eventos suportados:
    - login_fail    → falha de autenticação
    - 403           → acesso negado
    - 404           → recurso não encontrado
    - bruteforce    → tentativa de força bruta
    - blocked       → acesso bloqueado
    - suspicious    → atividade suspeita
    - invalid_csrf  → falha validação CSRF

    Exemplos de uso:
    - Monitoramento de ataques
    - Detecção de abuso
    - Logs de segurança
    - Integração com alertas
    - Dashboards administrativos
    - Estatísticas de eventos críticos

    Arquitetura:
    Os registros devem ser gerados preferencialmente por:
    - middlewares
    - signals de autenticação
    - decorators de permissão
    - handlers de exceção
    - services/security_service.py

    Boas práticas:
    - NÃO registrar informações sensíveis
    - Evitar armazenar payloads completos
    - Filtrar bots conhecidos quando necessário
    - Registrar IP real via proxy reverso
    - Limitar retenção de logs antigos

    Integrações futuras:
    - Fail2Ban
    - Grafana
    - Loki
    - ElasticSearch
    - SIEM
    - OpenTelemetry

    Observações:
    - O campo metadata permite extensibilidade
    - Os índices foram adicionados para otimizar consultas
    - Recomendado uso com HTTPS e proxy reverso

    Autor: Janer
    """

    EVENT_LOGIN_FAIL = 'login_fail'
    EVENT_403 = '403'
    EVENT_404 = '404'
    EVENT_BRUTEFORCE = 'bruteforce'
    EVENT_BLOCKED = 'blocked'
    EVENT_SUSPICIOUS = 'suspicious'
    EVENT_INVALID_CSRF = 'invalid_csrf'

    CHOICES_EVENT = (
        (EVENT_LOGIN_FAIL, 'Falha de Login'),
        (EVENT_403, 'Acesso Negado'),
        (EVENT_404, 'Página Não Encontrada'),
        (EVENT_BRUTEFORCE, 'Brute Force'),
        (EVENT_BLOCKED, 'Acesso Bloqueado'),
        (EVENT_SUSPICIOUS, 'Atividade Suspeita'),
        (EVENT_INVALID_CSRF, 'CSRF Inválido'),
    )

    site = models.ForeignKey(
        'a_Site.Site',
        on_delete=models.CASCADE,
        related_name='security_logs',
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='security_logs'
    )
    event = models.CharField(
        max_length=50,
        choices=CHOICES_EVENT
    )
    severity = models.CharField(
        max_length=20,
        default='medium',
        help_text='low, medium, high, critical'
    )
    ip = models.GenericIPAddressField()
    path = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )
    method = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )
    user_agent = models.TextField(
        blank=True,
        null=True
    )
    referer = models.TextField(
        blank=True,
        null=True
    )
    message = models.TextField(
        blank=True,
        null=True
    )
    metadata = models.JSONField(
        default=dict,
        blank=True
    )
    is_bot = models.BooleanField(
        default=False
    )
    create_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        db_table = 'a_log_security'
        verbose_name = 'Log de Segurança'
        verbose_name_plural = 'Logs de Segurança'
        ordering = ['-create_at']
        indexes = [
            models.Index(
                fields=['event']
            ),
            models.Index(
                fields=['ip']
            ),
            models.Index(
                fields=['user']
            ),
            models.Index(
                fields=['create_at']
            ),
            models.Index(
                fields=['severity']
            ),
        ]

    def __str__(self):

        return (
            f'{self.event} - '
            f'{self.ip}'
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
            'event': self.event,
            'severity': self.severity,
            'ip': self.ip,
            'path': self.path,
            'method': self.method,
            'user_agent': self.user_agent,
            'referer': self.referer,
            'message': self.message,
            'is_bot': self.is_bot,
            'metadata': self.metadata,
            'create_at': self.create_at.isoformat()
        }