from django.utils.translation import gettext_lazy as _

from wagtail_modeladmin.options import (
    modeladmin_register,
    ModelAdminGroup,
)

from wagtail.snippets.models import register_snippet
from wagtail_localize.modeladmin.options import TranslatableModelAdmin

from parat.footer.models import FooterColumn, FooterBottomItem


class FooterColumnAdmin(TranslatableModelAdmin):
    model = FooterColumn
    menu_order = 1

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("items")

    list_display = ["title", "ordering", "all_items"]

    def all_items(self, obj):
        return [str(o) for o in obj.items.all()]


class FooterBottomItemAdmin(TranslatableModelAdmin):
    model = FooterBottomItem
    menu_order = 2
    list_display = ["title", "page", "url"]


class FooterAdminGroup(ModelAdminGroup):
    menu_label = _("Footer")
    menu_icon = "doc-full"
    menu_order = 500
    items = [FooterColumnAdmin, FooterBottomItemAdmin]


register_snippet(FooterColumn)

modeladmin_register(FooterAdminGroup)
