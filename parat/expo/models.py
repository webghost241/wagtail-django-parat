from collections import defaultdict

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.translation import gettext_lazy as _

# Create your models here.
from wagtail.admin.panels import FieldPanel

from parat.core.models import AbstractBaseModel, StandardPage
from parat.core.models.wagtail import AbstractStandardPage


class ExpoCategory(AbstractBaseModel):
    label = models.CharField(
        null=False, blank=False, unique=True, max_length=255, verbose_name=_("Label")
    )

    def __str__(self):
        return self.label


class Expo(AbstractBaseModel):
    categories = models.ManyToManyField(ExpoCategory, verbose_name=_("Kategorien"))
    start_date = models.DateField(verbose_name=_("Startdatum"))
    end_date = models.DateField(verbose_name=_("Enddatum"))
    title = models.CharField(
        null=False, blank=False, unique=True, max_length=255, verbose_name=_("Titel")
    )
    city = models.CharField(
        null=False, blank=False, max_length=255, verbose_name=_("Stadt")
    )
    venue_location = models.CharField(
        null=False, blank=False, max_length=255, verbose_name=_("Standort am Venue")
    )
    url = models.URLField(blank=False, verbose_name=_("URL"))
    url_label = models.CharField(
        blank=True, max_length=255, verbose_name=_("URL Label")
    )
    image = models.ForeignKey(
        null=False,
        blank=False,
        to="wagtailimages.image",
        related_name="+",
        on_delete=models.PROTECT,
    )
    panels = [
        FieldPanel("categories"),
        FieldPanel("title"),
        FieldPanel("start_date"),
        FieldPanel("end_date"),
        FieldPanel("city"),
        FieldPanel("venue_location"),
        FieldPanel("url"),
        FieldPanel("url_label"),
        FieldPanel("image"),
    ]

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.title} ({self.start_date}-{self.end_date})"

    @property
    def formatted_date(self) -> str:
        """
        Returns start and enddate formatted so that only the necessary fields are shown.
        e.g. 09-10 September 2023
        """
        if self.start_date == self.end_date:
            return date_format(self.start_date, format="d. F Y", use_l10n=True)
        if self.start_date.month == self.end_date.month:
            return f"{date_format(self.start_date, 'd.')} – {date_format(self.end_date, 'd. F Y')}"
        if self.start_date.year == self.end_date.year:
            return f"{date_format(self.start_date, 'd. F')} – {date_format(self.end_date, 'd. F Y')}"
        return f"{date_format(self.start_date, 'd. F Y')} – {date_format(self.end_date, 'd. F Y')}"


class ExpoPage(AbstractStandardPage):
    def get_context(self, request, *args, **kwargs):
        expos = (
            Expo.objects.filter(end_date__gte=timezone.now())
            .prefetch_related("categories")
            .select_related("image")
            .order_by("start_date")
        )
        months_expo_dict = defaultdict(
            list
        )  # defaultdict needs to transformed back to normal dict for use in context
        context = super().get_context(request, *args, **kwargs)
        from parat.expo.filters import (
            ExpoFilter,
        )  # need to locally import to avoid circular import

        f: ExpoFilter = ExpoFilter(request.GET, queryset=expos)
        paginator = Paginator(f.qs, 10)
        page = request.GET.get("page")
        try:
            expo_page = paginator.page(page)
        except PageNotAnInteger:
            expo_page = paginator.page(1)
        except EmptyPage:
            expo_page = paginator.page(paginator.num_pages)
        for expo in expo_page:
            formatted_month = date_format(expo.start_date, format="F Y", use_l10n=True)
            months_expo_dict[formatted_month].append(expo)

        context["months_expo_dict"] = dict(months_expo_dict)
        context.update(
            months_expo_dict=dict(months_expo_dict),
            filter=f,
            pagination_object=expo_page,
            c_chosen=request.GET.get("c"),
        )
        return context
