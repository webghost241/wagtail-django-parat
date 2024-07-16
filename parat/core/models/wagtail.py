import urllib

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtailseo.models import SeoMixin

from parat.core.blocks import BaseStreamBlock, ContentFieldFactory, HeroBlock

__all__ = ["FormField", "FormPage", "StandardPage"]


def get_image_model_path() -> str:
    return getattr(settings, "WAGTAILIMAGES_IMAGE_MODEL", "wagtailimages.Image")


class FormField(AbstractFormField):
    page = ParentalKey("FormPage", related_name="form_fields", on_delete=models.CASCADE)


class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro"),
        InlinePanel("form_fields", label=_("core.models.formpage_inline_panel_label")),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            "Email",
        ),
    ]


class HomePage(SeoMixin, Page):
    promote_panels = SeoMixin.seo_panels

    """
    The parat home page
    """

    heading = models.TextField(
        help_text=_("Pre-Headline"), verbose_name=_("Pre-Headline"), blank=True
    )
    subheading = models.TextField(
        help_text=_("Headline"), verbose_name=_("Headline"), blank=True
    )
    header_image = models.ForeignKey(
        get_image_model_path(),
        verbose_name=_("Header Image"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = ContentFieldFactory().get_general_body()

    content_panels = Page.content_panels + [
        FieldPanel("heading"),
        FieldPanel("subheading"),
        FieldPanel("header_image"),
        FieldPanel("body"),
    ]

    @property
    def seo_pagetitle(self: Page) -> str:
        return f"{self.title} | PARAT Solutions"

    @property
    def seo_canonical_url(self: Page) -> str:
        return self.canonical_url

    @property
    def seo_image_url(self: Page) -> str:
        super_url = super().seo_image_url
        if super_url == "":
            return ""

        path = urllib.parse.urlparse(super_url).path
        return f"{self.canonical_base_url}{path}"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        self.canonical_base_url = f"https://{request.get_host()}"
        self.canonical_url = f"{self.canonical_base_url}{request.path}"

        return context


class AbstractDefaultPage(SeoMixin, Page):
    promote_panels = SeoMixin.seo_panels
    template = "core/standard_page.html"

    """
    A generic content page that can be used for any type of page content that
    only needs a title, and body
    """

    header_image = models.ForeignKey(
        get_image_model_path(),
        verbose_name=_("Header Image"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = ContentFieldFactory().get_general_body()
    content_panels = Page.content_panels + [
        FieldPanel("header_image"),
        FieldPanel("body", heading=_("Content")),
    ]

    @property
    def seo_pagetitle(self: Page) -> str:
        return f"{self.seo_title or self.title} | PARAT Solutions"

    @property
    def seo_canonical_url(self: Page) -> str:
        return self.canonical_url

    @property
    def seo_image_url(self: Page) -> str:
        super_url = super().seo_image_url
        if super_url == "":
            return ""

        path = urllib.parse.urlparse(super_url).path
        return f"{self.canonical_base_url}{path}"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        self.canonical_base_url = f"https://{request.get_host()}"
        self.canonical_url = f"{self.canonical_base_url}{request.path}"

        return context

    class Meta:
        abstract = True


class AbstractStandardPage(AbstractDefaultPage):
    introduction_headline = models.CharField(
        max_length=255, null=False, blank=False, verbose_name=_("Pre-Headline")
    )
    introduction_subheadline = models.CharField(
        max_length=255, null=False, blank=False, verbose_name=_("Headline")
    )
    introduction_text = RichTextField(
        blank=True,
        null=True,
        verbose_name=_("Eingangstext"),
        help_text=_("Text unter der Headline"),
    )
    content_panels = [
        FieldPanel("title"),
        FieldPanel("introduction_headline"),
        FieldPanel("introduction_subheadline"),
        FieldPanel("introduction_text"),
    ] + list(
        filter(lambda p: p.field_name != "title", AbstractDefaultPage.content_panels)
    )
    """
    A generic content page that can be used for any type of page content that
    only needs a title, and body
    """

    class Meta:
        abstract = True


class StandardPage(AbstractStandardPage):
    card_image = models.ForeignKey(
        get_image_model_path(),
        verbose_name=_("Card Image"),
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="+",
    )

    content_panels = AbstractStandardPage.content_panels + [
        FieldPanel("card_image"),
    ]


class DataProtectionPage(AbstractDefaultPage):
    max_count = 1
    template = "core/dataprotection_page.html"
    parent_page_types = ["HomePage"]


class ImprintPage(AbstractDefaultPage):
    max_count = 1
    template = "core/imprint_page.html"
    parent_page_types = ["HomePage"]
