import os
import shutil

from decimal import Decimal

from django.conf import settings
from django.utils import timezone

from a_Log.models.storage import StorageLog


class MediaStorageService:
    """
    Serviço responsável pelo monitoramento do armazenamento
    de mídia do CMS.

    Objetivos:
    - Monitorar espaço utilizado
    - Calcular percentual de uso
    - Gerar snapshots históricos
    - Apoiar dashboards administrativos
    - Auxiliar políticas de quota

    Funcionalidades:
    - análise do MEDIA_ROOT
    - cálculo da partição
    - total arquivos
    - histórico de crescimento
    """

    @classmethod
    def get_storage_info(cls):
        """
        Retorna métricas do armazenamento.
        """

        media_root = settings.MEDIA_ROOT
        total, used, free = shutil.disk_usage(
            media_root
        )
        media_used_bytes = cls.get_directory_size(
            media_root
        )
        partition_total_gb = cls.bytes_to_gb(
            total
        )
        partition_used_gb = cls.bytes_to_gb(
            used
        )
        partition_free_gb = cls.bytes_to_gb(
            free
        )
        media_used_gb = cls.bytes_to_gb(
            media_used_bytes
        )
        partition_percent_used = (
            (used / total) * 100
            if total > 0
            else 0
        )
        media_percent_used = (
            (media_used_bytes / total) * 100
            if total > 0
            else 0
        )
        total_files = cls.count_files(
            media_root
        )

        return {
            'path': media_root,
            'partition_total_gb': round(
                partition_total_gb,
                2
            ),
            'partition_used_gb': round(
                partition_used_gb,
                2
            ),
            'partition_free_gb': round(
                partition_free_gb,
                2
            ),
            'partition_percent_used': round(
                partition_percent_used,
                2
            ),
            'media_used_gb': round(
                media_used_gb,
                2
            ),
            'media_percent_used': round(
                media_percent_used,
                2
            ),
            'total_files': total_files,
        }


    @classmethod
    def register_snapshot(
        cls,
        site=None,
        storage_type=StorageLog.TYPE_MEDIA,
        metadata=None
    ):
        """
        Registra snapshot histórico do storage.
        """

        storage = cls.get_storage_info()
        return StorageLog.objects.create(
            site=site,
            storage_type=storage_type,
            path=storage['path'],
            partition_total_gb=Decimal(
                storage['partition_total_gb']
            ),
            partition_used_gb=Decimal(
                storage['partition_used_gb']
            ),
            partition_free_gb=Decimal(
                storage['partition_free_gb']
            ),
            partition_percent_used=Decimal(
                storage['partition_percent_used']
            ),
            storage_used_gb=Decimal(
                storage['media_used_gb']
            ),
            storage_percent_used=Decimal(
                storage['media_percent_used']
            ),
            total_files=storage['total_files'],
            metadata=metadata or {},
            create_at=timezone.now()
        )


    @staticmethod
    def get_directory_size(path):
        """
        Calcula tamanho total do diretório.
        """
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(
                    dirpath,
                    filename
                )
                try:
                    total_size += os.path.getsize(
                        filepath
                    )
                except (
                    FileNotFoundError,
                    PermissionError
                ):
                    continue

        return total_size


    @staticmethod
    def count_files(path):
        """
        Conta quantidade total de arquivos.
        """
        total = 0
        for _, _, files in os.walk(path):
            total += len(files)
        return total


    @staticmethod
    def bytes_to_gb(value):
        """
        Converte bytes para gigabytes.
        """

        return value / (
            1024 * 1024 * 1024
        )