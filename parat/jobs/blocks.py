import django.urls
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import CharBlock, PageChooserBlock, StructBlock
from wagtail.models import Locale

from parat.core.blocks import BaseLayoutBlock


class JobBlock(StructBlock):
    job = PageChooserBlock(page_type="jobs.JobPage")

    class Meta:
        template = "blocks/job_block.html"


class JobListBlock(BaseLayoutBlock):
    title = CharBlock(max_length=255)
    link_text = CharBlock(max_length=255, default="See More")

    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(local_blocks=[("Job", JobBlock(local_blocks))])

    class Meta:
        template = "blocks/job_list_block.html"

    def get_context(self, value: "JobListBlock", parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        return context


class DynamicJobListBlock(BaseLayoutBlock):
    title = CharBlock(max_length=255)
    link_text = CharBlock(max_length=255)

    class Meta:
        template = "blocks/dynamic_job_list_block.html"

    def get_context(self, value: "DynamicJobListBlock", parent_context=None):
        context = super().get_context(value, parent_context)
        from parat.jobs.models import JobPage

        jobs = JobPage.objects.filter(locale=Locale.get_active()).live()
        context["self"].update(jobs=jobs)
        return context
