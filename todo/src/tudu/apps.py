from django.apps import AppConfig


class TuduConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tudu'

    def ready(self):
        import tudu.signals
