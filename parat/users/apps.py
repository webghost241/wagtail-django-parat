from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "parat.users"
    verbose_name = _("users.apps.verbose_name")

    def ready(self):
        try:
            import parat.users.signals  # noqa F401
        except ImportError:
            pass
