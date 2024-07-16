from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import PageChooserPanel, FieldPanel, InlinePanel
from wagtail.models import TranslatableMixin, Orderable

from parat.core.models import AbstractBaseModel


class FooterColumn(TranslatableMixin, AbstractBaseModel, ClusterableModel):
    title = models.CharField(max_length=64, verbose_name=_("Titel"))
    page = models.ForeignKey(
        to="wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name=_("Seite"),
    )
    url = models.URLField(verbose_name=_("Url"), blank=True, null=True)
    ordering = models.SmallIntegerField(blank=False, null=False)

    panels = [
        FieldPanel("title"),
        PageChooserPanel("page"),
        FieldPanel("url"),
        FieldPanel("ordering"),
        InlinePanel("items", label=_("Items")),
    ]

    class Meta:
        unique_together = [("translation_key", "locale")]
        ordering = ["ordering", "title"]

    @property
    def link(self):
        url = dict()
        if self.page:
            url.update(url=self.page.localized.url, external=False)
        elif self.url:
            url.update(url=self.url, external=True)
        return url

    def clean(self):
        # Column head can be not linking to anything
        pass

    def __str__(self):
        return self.title


class FooterItem(TranslatableMixin, Orderable, AbstractBaseModel):
    column = ParentalKey(
        FooterColumn,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name=_("Spalte"),
        related_name="items",
    )
    title = models.CharField(max_length=64, verbose_name=_("Titel"))
    page = models.ForeignKey(
        to="wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name=_("Seite"),
    )
    url = models.URLField(verbose_name=_("Url"), blank=True, null=True)
    icon_name = models.CharField(
        max_length=32, help_text=_("Bootstrap icon name"), blank=True, null=True
    )

    class Meta:
        ordering = ["sort_order"]
        unique_together = [("translation_key", "locale")]

    @property
    def link(self):
        url = dict()
        if self.page:
            url.update(url=self.page.localized.url, external=False)
        else:
            url.update(url=self.url, external=True)
        return url

    def clean(self):
        if not self.page and not self.url:
            raise ValidationError(_("Entweder Seite oder Url müssen gesetzt werden"))

    content_panels = panels = [
        FieldPanel("title"),
        PageChooserPanel("page"),
        FieldPanel("url"),
        FieldPanel("icon_name"),
    ]

    def __str__(self):
        return self.title


class FooterBottomItem(TranslatableMixin, AbstractBaseModel):
    title = models.CharField(max_length=64, verbose_name=_("Titel"))
    page = models.ForeignKey(
        to="wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name=_("Seite"),
    )
    url = models.URLField(verbose_name=_("Url"), blank=True, null=True)
    ordering = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["ordering", "title"]
        unique_together = [("translation_key", "locale")]

    @property
    def link(self):
        if self.page:
            return self.page.localized.url
        if self.url:
            return self.url
        return None

    content_panels = panels = [
        FieldPanel("title"),
        PageChooserPanel("page"),
        FieldPanel("url"),
        FieldPanel("ordering"),
    ]

    def __str__(self):
        return self.title
