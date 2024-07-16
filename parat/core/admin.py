from django.contrib.admin import ModelAdmin


class AbstractBaseModelAdmin(ModelAdmin):
    """
    Provides a BaseAdmin that add updated_at and created as readonly fields

    Example-Usage:
    from django.contrib import admin
    from <app>.models import ModelA, ModelB

    @admin.register(ModelA, ModelB)
    class BaseModelAdmin(AbstractBaseModelAdmin):
        pass
    """

    readonly_fields = ["updated_at", "created_at"]
