import os
from functools import partial

from django.core.validators import FileExtensionValidator
from django.db import models
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.documents import get_document_model
from wagtail.models import Page

from parat.core.models import StandardPage
from parat.core.util.fileutil import upload_generic_namer
from .blocks import JobListBlock, DynamicJobListBlock
from ..core.blocks import ContentFieldFactory
from ..core.models.wagtail import (
    AbstractStandardPage,
)


class JobIndexPage(AbstractStandardPage):
    body = (
        ContentFieldFactory()
        .set_extra_blocks(
            [
                ("job_list_block", JobListBlock()),
                ("dynamic_job_list_block", DynamicJobListBlock()),
            ]
        )
        .get_general_body()
    )


class JobPage(Page):
    headline = models.CharField(
        max_length=255,
        null=False,
        blank=False,
    )
    short_description = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        help_text=_("Kurzbeschreibung für Listenansicht"),
    )
    file = models.ForeignKey(
        to=get_document_model(),
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )

    content_panels = Page.content_panels + [
        FieldPanel("headline"),
        FieldPanel("short_description"),
        FieldPanel("file"),
    ]

    def serve(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.file.url)

    parent_page_types = ["jobs.JobIndexPage"]
