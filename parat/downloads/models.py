from collections import defaultdict

import pycountry
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from django.utils.translation import get_language, gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.documents import get_document_model
from wagtail.models import Orderable, Page, TranslatableMixin

from parat.core.models import AbstractBaseModel
from parat.core.models.wagtail import AbstractDefaultPage, AbstractStandardPage

class DownloadGroup(AbstractBaseModel, ClusterableModel):
    label_de = models.CharField(
        max_length=255, null=False, blank=False, unique=True, verbose_name=_("Label Deutsch")
    )
    label_en = models.CharField(
        max_length=255, null=True, blank=True, unique=True, verbose_name=_("Label Englisch")
    )
    ordering = models.SmallIntegerField(verbose_name=_("Ordering"))

    panels = [
        FieldPanel("label_de"),
        FieldPanel("label_en"),
        FieldPanel("ordering"),
        InlinePanel("downloads"),
    ]

    def get_label(self):
        lang = get_language()
        if lang not in ("en", "de"):
            return self.lang_de
        return getattr(self, f"label_{lang}")

    class Meta:
        ordering = ["ordering"]

    def __str__(self):
        return str(self.get_label())


class DownloadLanguage(ClusterableModel, AbstractBaseModel):
    label = models.CharField(
        max_length=64,
        null=False,
        blank=False,
        unique=True,
        verbose_name=_("Label"),
        choices=[
            (l.name, l.name)
            for l in list(sorted(pycountry.languages, key=lambda x: x.name))
        ],
    )
    alpha_2 = models.CharField(
        max_length=3,
        null=False,
        blank=False,
        unique=True,
        verbose_name=_("Sprachkürzel"),
        help_text=_("z.B. DE"),
    )

    def save(self, **kwargs):
        self.alpha_2 = pycountry.languages.get(name=self.label).alpha_2
        super().save(**kwargs)

    def __str__(self):
        return f"{self.alpha_2.upper()} {self.label}"


class Download(AbstractBaseModel):
    download_group = ParentalKey(
        to=DownloadGroup,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        verbose_name=_("Gruppe"),
        related_name="downloads",
    )
    download_languages = models.ManyToManyField(
        to=DownloadLanguage, blank=False, verbose_name=_("Sprachen")
    )
    title = models.CharField(
        max_length=255, null=False, blank=False, verbose_name=_("Titel")
    )
    description = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Beschreibung")
    )
    file = models.ForeignKey(
        null=False,
        blank=False,
        to=get_document_model(),
        on_delete=models.PROTECT,
    )

    panels = [
        FieldPanel("download_group"),
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("download_languages"),
        FieldPanel("file"),
    ]

    def __str__(self):
        return self.title


class DownloadIndexPage(AbstractStandardPage):
    content_panels = Page.content_panels + [
        FieldPanel("header_image"),
        FieldPanel("introduction_headline"),
        FieldPanel("introduction_subheadline"),
        FieldPanel("introduction_text"),
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        all_downloads = Download.objects.order_by(
            "download_group", "title"
        ).prefetch_related("download_group", "download_languages")
        from parat.downloads.filters import DownloadFilter

        f: DownloadFilter = DownloadFilter(
            request.GET, queryset=all_downloads
        )  # need to locally import to avoid circular import
        paginator = Paginator(f.qs, 10)
        page = request.GET.get("page")
        try:
            downloads_page = paginator.page(page)
        except PageNotAnInteger:
            downloads_page = paginator.page(1)
        except EmptyPage:
            downloads_page = paginator.page(paginator.num_pages)

        downloads_by_category = defaultdict(list)
        for download in downloads_page:
            downloads_by_category[download.download_group.get_label()].append(download)
        context.update(
            pagination_object=downloads_page,
            downloads_by_category_dict=dict(downloads_by_category),
            filter=f,
            l_chosen=request.GET.get("l"),
            c_chosen=request.GET.get("c"),
        )
        return context
