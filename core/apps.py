from django.apps import AppConfig
from .forms import StaffUserCreationForm


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        import core.signals  