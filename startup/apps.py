from django.apps import AppConfig


class StartupConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'startup'

    def ready(self) -> None:
        import startup.signals