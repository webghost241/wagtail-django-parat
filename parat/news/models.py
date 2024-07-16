from collections import namedtuple
from urllib.parse import urlunparse

from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.utils.translation import gettext as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from puput.models import BlogPage, EntryPage
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.documents import get_document_model

from parat.core.models import AbstractBaseModel


def get_image_model_path() -> str:
    return getattr(settings, "WAGTAILIMAGES_IMAGE_MODEL", "wagtailimages.Image")


Components = namedtuple(
    typename="Components",
    field_names=["scheme", "netloc", "url", "path", "query", "fragment"],
)


class ParatEntryPage(EntryPage, ClusterableModel):
    parent_page_types = ["ParatBlogPage"]
    subtitle = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Subtitel")
    )

    content_panels = [*EntryPage.content_panels]
    main_content_panel = content_panels[0]
    # # remove the Markdown input panel
    main_content_panel.children.pop(3)

    content_panels = content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("subtitle"),
                InlinePanel("documents", label=_("Anhänge")),
            ],
            heading=_("PARAT"),
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        context.update(
            download_documents=ParatEntryDocument.objects.filter(parat_entry=self),
        )
        return context

    @property
    def page_url(self):
        return urlunparse(
            Components(
                scheme="https",
                netloc=f"www.{settings.WAGTAILADMIN_BASE_URL}",
                query="",
                path="",
                url=self.url,
                fragment="",
            )
        )

    class Meta:
        verbose_name = _("PARAT Beitrag")


class ParatEntryDocument(AbstractBaseModel):
    document = models.ForeignKey(
        get_document_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Dokument"),
    )

    label = models.CharField(
        null=True, blank=False, verbose_name=_("Beschriftung"), max_length=255
    )

    parat_entry = ParentalKey(
        ParatEntryPage,
        related_name="documents",
        on_delete=models.CASCADE,
    )


class ParatBlogPage(BlogPage):
    subpage_types = ["ParatEntryPage"]
    introduction_subheadline = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name=_("Headline"),
        default=_("Immer Aktuell"),
    )
    card_image = models.ForeignKey(
        get_image_model_path(),
        verbose_name=_("Card Image"),
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="+",
    )
    # do not show header image and main color as they have no effect!
    # content_panels = list(
    #     filter(
    #         lambda p: p.field_name not in ["header_image", "main_color"],
    #         BlogPage.content_panels,
    #     )
    # )

    content_panels = BlogPage.content_panels + [
        FieldPanel("introduction_subheadline"),
        FieldPanel("card_image"),
    ]

    def get_entries(self):
        return (
            ParatEntryPage.objects.descendant_of(self)
            .live()
            .order_by("-date")
            .select_related("owner")
        )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        paginator = Paginator(
            ParatEntryPage.objects.descendant_of(self)
            .live()
            .order_by("-date")
            .select_related("owner")[1:],
            3,
        )
        page = request.GET.get("page")

        try:
            news_page = paginator.page(page)
        except PageNotAnInteger:
            news_page = paginator.page(1)
        except EmptyPage:
            news_page = paginator.page(paginator.num_pages)

        context.update(pagination_object=news_page)

        return context

    class Meta:
        verbose_name = _("Parat Blog Page")
