from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from .models import Download, DownloadGroup, DownloadLanguage


class DownloadGroupAdmin(ModelAdmin):
    model = DownloadGroup
    menu_order = 1
    menu_icon = "tag"


class DownloadLanguageAdmin(ModelAdmin):
    model = DownloadLanguage
    menu_order = 3
    menu_icon = "comment"
    form_fields_exclude = ["alpha_2"]


class DownloadAdmin(ModelAdmin):
    model = Download
    menu_label = _("Downloads")
    menu_icon = "doc-full"
    menu_order = 2
    add_to_admin_menu = True  # or False to exclude your model from the menu
    list_display = (
        "download_group",
        "title",
        "description",
        "file",
        "download_languages",
    )
    list_filter = ("download_group", "download_languages")
    search_fields = ("title",)


class DownloadAdminGroup(ModelAdminGroup):
    menu_label = _("Downloads")
    menu_icon = "doc-full"
    menu_order = 400
    items = (DownloadAdmin, DownloadGroupAdmin, DownloadLanguageAdmin)


modeladmin_register(DownloadAdminGroup)
