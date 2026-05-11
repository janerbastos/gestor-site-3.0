from django.db import models


class StorageLog(models.Model):

    """
    Modelos de armazenamento e monitoramento de uso de disco.

    Este módulo é responsável por registrar métricas relacionadas ao
    armazenamento do CMS, permitindo monitoramento contínuo do consumo
    de espaço utilizado por mídias, backups e arquivos temporários.

    Objetivos:
    - Monitorar uso do MEDIA_ROOT
    - Calcular percentual de utilização
    - Registrar espaço livre e total da partição
    - Gerar histórico de crescimento do storage
    - Auxiliar dashboards administrativos
    - Apoiar políticas de quota e limpeza automática

    Tipos suportados:
    - media   → arquivos enviados por usuários
    - backup  → backups do sistema
    - temp    → arquivos temporários/cache

    Exemplos de uso:
    - Dashboard administrativo
    - Alertas de disco cheio
    - Estatísticas de crescimento
    - Auditoria de armazenamento
    - Relatórios operacionais

    Arquitetura:
    O modelo deve ser alimentado preferencialmente por:
    - services/storage_service.py
    - tasks periódicas (Celery/Cron)

    Observações:
    - NÃO armazena arquivos
    - Apenas métricas e snapshots históricos
    - Ideal para agregação temporal

    Autor: Janer
    """

    TYPE_MEDIA = 'media'
    TYPE_BACKUP = 'backup'
    TYPE_TEMP = 'temp'

    CHOICES_TYPE = (
        (TYPE_MEDIA, 'Mídia'),
        (TYPE_BACKUP, 'Backup'),
        (TYPE_TEMP, 'Temporário'),
    )

    site = models.ForeignKey(
        'a_Site.Site',
        on_delete=models.CASCADE,
        related_name='storage_logs',
        null=True,
        blank=True
    )
    storage_type = models.CharField(
        max_length=20,
        choices=CHOICES_TYPE,
        default=TYPE_MEDIA
    )
    path = models.CharField(
        max_length=500,
        help_text='Caminho monitorado'
    )
    partition_total_gb = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    partition_used_gb = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    partition_free_gb = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    partition_percent_used = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )
    storage_used_gb = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    storage_percent_used = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )
    total_files = models.PositiveBigIntegerField(
        default=0
    )
    metadata = models.JSONField(
        default=dict,
        blank=True
    )
    create_at = models.DateTimeField(
        auto_now_add=True
    )
    class Meta:

        db_table = 'a_log_storage'
        verbose_name = 'Log de Armazenamento'
        verbose_name_plural = 'Logs de Armazenamento'
        ordering = ['-create_at']
        indexes = [
            models.Index(
                fields=['site']
            ),
            models.Index(
                fields=['storage_type']
            ),
            models.Index(
                fields=['create_at']
            ),
        ]

    def __str__(self):

        return (
            f'{self.storage_type} - '
            f'{self.storage_used_gb} GB'
        )

    def json(self):

        return {
            'id': self.id,
            'site': self.site_id,
            'storage_type': self.storage_type,
            'path': self.path,
            'partition_total_gb': float(
                self.partition_total_gb
            ),
            'partition_used_gb': float(
                self.partition_used_gb
            ),
            'partition_free_gb': float(
                self.partition_free_gb
            ),
            'partition_percent_used': float(
                self.partition_percent_used
            ),
            'storage_used_gb': float(
                self.storage_used_gb
            ),
            'storage_percent_used': float(
                self.storage_percent_used
            ),
            'total_files': self.total_files,
            'metadata': self.metadata,
            'create_at': self.create_at.isoformat()
        }