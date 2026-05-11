from django.conf import settings

import os
import shutil


class MediaStorageService:

    @staticmethod
    def get_storage_info():

        path_storage = settings.MEDIA_ROOT if settings.MEDIA_ROOT else '/home/adminsite/workspace/python/gestorsites-3.0/file'

        total, used, free = shutil.disk_usage(
            path_storage
        )

        media_size = 0

        for dirpath, dirnames, filenames in os.walk(
            path_storage
        ):

            for filename in filenames:

                filepath = os.path.join(
                    dirpath,
                    filename
                )

                if os.path.exists(filepath):

                    media_size += os.path.getsize(
                        filepath
                    )

        gb = 1024 ** 3

        media_percent = (
            (media_size / total) * 100
            if total > 0
            else 0
        )

        return {

            'partition_total_gb': round(
                total / gb,
                2
            ),

            'partition_free_gb': round(
                free / gb,
                2
            ),

            'media_used_gb': round(
                media_size / gb,
                2
            ),

            'media_percent_used': round(
                media_percent,
                2
            )
        }