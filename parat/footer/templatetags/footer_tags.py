from django import template
from django.utils.translation import get_language
from wagtail.models import Locale

from parat.footer.models import FooterColumn, FooterBottomItem

register = template.Library()


@register.inclusion_tag("footer/footer.html", takes_context=True)
def footer_tag(context):
    locale = Locale.objects.get_for_language(get_language())
    footer_columns = FooterColumn.objects.filter(locale=locale)
    footer_bottom_items = FooterBottomItem.objects.filter(locale=locale)
    return {
        "footer_columns": footer_columns,
        "footer_bottom_items": footer_bottom_items,
        "request": context["request"],
    }
