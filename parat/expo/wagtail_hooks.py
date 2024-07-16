from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
    ModelAdminGroup,
)

from parat.expo.models import ExpoCategory, Expo


class ExpoCategoryAdmin(ModelAdmin):
    model = ExpoCategory
    menu_order = 1
    menu_icon = "tag"
    menu_label = _("Messe-Kategorien")


class ExpoAdmin(ModelAdmin):
    model = Expo
    menu_order = 2
    menu_icon = "globe"
    menu_label = _("Messen")


class ExpoAdminGroup(ModelAdminGroup):
    menu_label = _("Messen")
    menu_order = 401
    menu_icon = "globe"
    items = (ExpoCategoryAdmin, ExpoAdmin)


modeladmin_register(ExpoAdminGroup)
