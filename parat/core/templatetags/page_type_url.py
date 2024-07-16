import logging
from logging import getLogger

from django import template
from django.apps import apps
from wagtailmenus.models import MenuPage

register = template.Library()


MenuPage

logger = getLogger(__name__)


@register.simple_tag(takes_context=True)
def page_type_url(context, app: str, pagetype: str):
    try:
        pageType = apps.get_model(app, pagetype)
        page = pageType.objects.live().first()
        if page:
            return page.localized
    except LookupError:
        logging.Logger.debug("LookupError")
    return None


@register.simple_tag()
def menu_item_link(item, page):
    try:
        if item.link_page and item.link_page.localized and item.link_page.localized.url:
            return item.link_page.localized.url
        else:
            if item.link_url:
                if not page:
                    return item.link_url
                elif page.locale.language_code == "en":
                    return item.link_url_en or item.link_url
                else:
                    return item.link_url
            else:
                return item.href
    except Exception as e:
        logger.error("Error while calculating link", exc_info=e)
        return ""
