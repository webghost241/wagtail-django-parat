from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.models import Page, TranslatableMixin
from wagtailmenus.models import (
    AbstractFlatMenu,
    AbstractFlatMenuItem,
    AbstractMainMenu,
    AbstractMainMenuItem,
)


class CustomMainMenu(AbstractMainMenu):
    def get_pages_for_display(self):
        """Returns a queryset of all pages needed to render the menu."""
        if hasattr(self, "_raw_menu_items"):
            # get_top_level_items() may have set this
            menu_items = self._raw_menu_items
        else:
            menu_items = self.get_base_menuitem_queryset()

        # Start with an empty queryset, and expand as needed
        queryset = Page.objects.none()

        for item in (item for item in menu_items if item.link_page):
            if item.link_page.localized:
                item.link_page = item.link_page.localized

            if (
                item.allow_subnav
                and item.link_page.depth >= settings.WAGTAILMENUS_SECTION_ROOT_DEPTH
            ):
                # Add this branch to the overall `queryset`
                queryset = queryset | Page.objects.filter(
                    path__startswith=item.link_page.path,
                    depth__lt=item.link_page.depth + self.max_levels,
                )
            else:
                # Add this page only to the overall `queryset`
                queryset = queryset | Page.objects.filter(id=item.link_page_id)

        # Filter out pages unsuitable display
        queryset = self.get_base_page_queryset() & queryset

        # Always return 'specific' page instances
        return queryset.specific()


class CustomMainMenuItem(AbstractMainMenuItem):
    """A minimal custom menu item model to be used by `LimitedMainMenu`.
    No additional fields / method necessary
    """

    menu = ParentalKey(
        CustomMainMenu,  # we can use the model from above
        on_delete=models.CASCADE,
        related_name=settings.WAGTAILMENUS_MAIN_MENU_ITEMS_RELATED_NAME,
    )

    link_url_en = models.URLField(blank=True)
    link_text_en = models.CharField(max_length=250, blank=True)
    link_open_new_tab = models.BooleanField(default=False, blank=False)
    panels = (
        PageChooserPanel("link_page"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel(
                            "link_text",
                            help_text=_("Gib einen Text für eine eigene URL an."),
                        ),
                        FieldPanel(
                            "link_url",
                            help_text=_(
                                "Gib eine URL ein auf die dieser Menüpunkt verweisen soll."
                            ),
                        ),
                    ],
                    heading=_("Deutsch"),
                ),
                FieldRowPanel(
                    [
                        FieldPanel(
                            "link_text_en",
                            help_text=_("Gib einen Text für eine eigene URL an."),
                        ),
                        FieldPanel(
                            "link_url_en",
                            help_text=_(
                                "Gib eine URL ein auf die dieser Menüpunkt verweisen soll."
                            ),
                        ),
                    ],
                    heading=_("Englisch"),
                ),
                FieldPanel("link_open_new_tab", heading=_("Link in neuem Tab öffnen.")),
            ],
            heading=_("Externe URL"),
        ),
        FieldPanel("url_append"),
        FieldPanel("allow_subnav"),
    )

    @property
    def is_external_link(self):
        return True if (self.link_url) else False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.link_page and self.link_page.localized:
            self.link_page = self.link_page.localized


class CustomFlatMenu(TranslatableMixin, AbstractFlatMenu):
    def get_pages_for_display(self):
        """Returns a queryset of all pages needed to render the menu."""
        if hasattr(self, "_raw_menu_items"):
            # get_top_level_items() may have set this
            menu_items = self._raw_menu_items
        else:
            menu_items = self.get_base_menuitem_queryset()

        # Start with an empty queryset, and expand as needed
        queryset = Page.objects.none()

        for item in (item for item in menu_items if item.link_page):
            if item.link_page.localized:
                item.link_page = item.link_page.localized

            if (
                item.allow_subnav
                and item.link_page.depth >= settings.WAGTAILMENUS_SECTION_ROOT_DEPTH
            ):
                # Add this branch to the overall `queryset`
                queryset = queryset | Page.objects.filter(
                    path__startswith=item.link_page.path,
                    depth__lt=item.link_page.depth + self.max_levels,
                )
            else:
                # Add this page only to the overall `queryset`
                queryset = queryset | Page.objects.filter(id=item.link_page_id)

        # Filter out pages unsuitable display
        queryset = self.get_base_page_queryset() & queryset

        # Always return 'specific' page instances
        return queryset.specific()


class CustomFlatMenuItem(TranslatableMixin, AbstractFlatMenuItem):
    menu = ParentalKey(
        CustomFlatMenu,  # we can use the model from above
        on_delete=models.CASCADE,
        related_name=settings.FLAT_MENU_ITEMS_RELATED_NAME,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.link_page and self.link_page.localized:
            self.link_page = self.link_page.localized
