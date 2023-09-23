from django.apps import AppConfig


class AbsusrConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'absusr'

    def ready(self):
        import absusr.signals
