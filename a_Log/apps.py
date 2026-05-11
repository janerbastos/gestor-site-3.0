from django.apps import AppConfig


class ALogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'a_Log'

    def ready(self):
        """
        Carrega signals da aplicação.
        """
        import a_Log.signals
