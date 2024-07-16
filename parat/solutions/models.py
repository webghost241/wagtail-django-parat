from django.conf import settings
from django.contrib import messages
from django.db import models
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField

from parat.core.blocks import COLUMN_HERO_STREAMBLOCKS, ContentFieldFactory
from parat.core.blocks.parat_blocks import HeadlineAndTextBlockWithVideo
from parat.core.models.wagtail import AbstractStandardPage
from parat.solutions.blocks import (
    DynamicSolutionBlock,
    ImageCollageBlock,
    ImageSliderBlock,
)


# TODO: move into util copy / pasted from parat/core/models/wagtail.py
def get_image_model_path() -> str:
    return getattr(settings, "WAGTAILIMAGES_IMAGE_MODEL", "wagtailimages.Image")


class SolutionIndexPage(AbstractStandardPage):
    subpage_types = ["SolutionPage"]
    body = (
        ContentFieldFactory()
        .set_extra_blocks(
            [
                ("headline_and_text_with_video", HeadlineAndTextBlockWithVideo()),
                ("image_slider_block", ImageSliderBlock()),
                ("image_collage_block", ImageCollageBlock()),
            ]
        )
        .get_general_body()
    )

    @property
    def solutions(self):
        return self.get_children().live().distinct().specific()

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        from parat.contact.forms import ContactForm

        context.update(form=ContactForm())
        return context

    def serve(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        if request.method == "POST":
            from parat.contact.forms import ContactForm

            form = ContactForm(request.POST)
            if form.is_valid():
                # do stuff
                form.save_and_send_out_mails(request)
                context["form"] = ContactForm()
                messages.success(
                    request,
                    _(
                        "Ihre Nachricht wurde erfolgreich versendet / Your Message was successfully sent"
                    ),
                )
            else:
                context["form"] = form
                context["show_contact_modal"] = True
        context["show_contact_modal"] = True

        return TemplateResponse(
            request=request,
            template=self.get_template(request, *args, **kwargs),
            context=context,
        )


class SolutionPage(AbstractStandardPage):
    parent_page_types = ["SolutionIndexPage"]
    subpage_types = ["SolutionApplicationPage"]

    body = StreamField(
        COLUMN_HERO_STREAMBLOCKS,
        null=True,
        blank=True,
        use_json_field=True,
    )

    @property
    def solutions(self):
        return (
            SolutionIndexPage.objects.ancestor_of(self)
            .first()
            .solutions.exclude(pk=self.pk)
        )
        # TODO: this seems prettier but somehow doesn't work
        # return self.get_parent().specific().solutions.exclude(pk=self.pk)

    @property
    def solution_index(self):
        ancestor = (
            SolutionIndexPage.objects.ancestor_of(self).order_by("-depth").first()
        )
        if ancestor:
            return ancestor
        else:
            return SolutionIndexPage.objects.first()

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        from parat.contact.forms import ContactForm

        context.update(form=ContactForm())
        return context

    def serve(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        if request.method == "POST":
            from parat.contact.forms import ContactForm

            form = ContactForm(request.POST)
            if form.is_valid():
                form.save_and_send_out_mails(request)
                context["form"] = ContactForm()
                messages.success(
                    request,
                    _(
                        "Ihre Nachricht wurde erfolgreich versendet / Your Message was successfully sent"
                    ),
                )
            else:
                context["form"] = form
                context["show_contact_modal"] = True
        return TemplateResponse(
            request=request,
            template=self.get_template(request, *args, **kwargs),
            context=context,
        )


class SolutionApplicationIndexPage(AbstractStandardPage):
    template = "solutions/solution_application_index_page.html"
    parent_page_types = ["SolutionIndexPage"]
    subpage_types = ["SolutionApplicationPage"]

    body = (
        ContentFieldFactory()
        .set_extra_blocks([("solution_cards", DynamicSolutionBlock())])
        .get_general_body()
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        from parat.contact.forms import ContactForm

        context.update(form=ContactForm())
        return context

    def serve(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        if request.method == "POST":
            from parat.contact.forms import ContactForm

            form = ContactForm(request.POST)
            if form.is_valid():
                form.save_and_send_out_mails(request)
                context["form"] = ContactForm()
                messages.success(
                    request,
                    _(
                        "Ihre Nachricht wurde erfolgreich versendet / Your Message was successfully sent"
                    ),
                )
            else:
                context["form"] = form
                context["show_contact_modal"] = True
        return TemplateResponse(
            request=request,
            template=self.get_template(request, *args, **kwargs),
            context=context,
        )


class SolutionApplicationPage(AbstractStandardPage):
    template = "solutions/solution_application_page.html"
    parent_page_types = ["SolutionApplicationIndexPage"]
    subpage_types = []
    card_headline = models.CharField(
        max_length=255, null=False, blank=False, verbose_name=_("Card-Headline")
    )
    card_subheadline = models.CharField(
        max_length=255, null=False, blank=False, verbose_name=_("Card-Sub-Headline")
    )
    card_text = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Kartentext"),
    )
    card_image = models.ForeignKey(
        get_image_model_path(),
        verbose_name=_("Card Image"),
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name="+",
    )

    body = (
        ContentFieldFactory()
        .set_extra_blocks([("solution_cards", DynamicSolutionBlock())])
        .get_general_body()
    )

    content_panels = AbstractStandardPage.content_panels + [
        FieldPanel("card_headline"),
        FieldPanel("card_subheadline"),
        FieldPanel("card_text"),
        FieldPanel("card_image"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        from parat.contact.forms import ContactForm

        context.update(form=ContactForm())
        return context

    def serve(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        if request.method == "POST":
            from parat.contact.forms import ContactForm

            form = ContactForm(request.POST)
            if form.is_valid():
                form.save_and_send_out_mails(request)
                context["form"] = ContactForm()
                messages.success(
                    request,
                    _(
                        "Ihre Nachricht wurde erfolgreich versendet / Your Message was successfully sent"
                    ),
                )
            else:
                context["form"] = form
                context["show_contact_modal"] = True
        return TemplateResponse(
            request=request,
            template=self.get_template(request, *args, **kwargs),
            context=context,
        )
