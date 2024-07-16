from typing import List, Optional, Tuple

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import (
    Block,
    BlockQuoteBlock,
    CharBlock,
    ChoiceBlock,
    PageChooserBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock,
    URLBlock,
)
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock

from .layout_blocks import SplitRowBlock


class ButtonBlock(StructBlock):
    page = PageChooserBlock(required=False, help_text=_("page to link to"))
    url = URLBlock(required=False, help_text=_("external URL to link to"))
    text = CharBlock(required=True, help_text=_("the text on the button"))
    style = ChoiceBlock(
        choices=settings.FRONTEND_BTN_STYLE_CHOICES,
        default=settings.FRONTEND_BTN_STYLE_DEFAULT,
        required=False,
        label=_("Button style"),
    )
    size = ChoiceBlock(
        choices=settings.FRONTEND_BTN_SIZE_CHOICES,
        default=settings.FRONTEND_BTN_SIZE_DEFAULT,
        required=False,
        label=_("Button size"),
    )

    class Meta:
        icon = "square"
        template = "blocks/button_block.html"


class ImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """

    image = ImageChooserBlock(required=True)
    # TODO: (c/sh)ould be renamed at a later point in time see:
    # https://gitlab.sphericalelephant.com/parat/parat/-/issues/139#note_94491
    attribution = CharBlock(
        required=False,
        help_text=_("alternativer Text wenn das Bild nicht angezeigt werden kann."),
        label=_("Alt Text"),
    )
    shadow = ChoiceBlock(
        choices=settings.FRONTEND_IMAGE_SHADOW_CHOICES,
        default=settings.FRONTEND_IMAGE_SHADOW_DEFAULT,
        required=False,
        label=_("Schatten"),
    )

    class Meta:
        icon = "image"
        template = "blocks/image_block.html"


class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """

    paragraph_block = RichTextBlock(icon="pilcrow")
    image_block = ImageBlock()
    block_quote = BlockQuoteBlock()
    embed_block = (
        EmbedBlock(
            help_text=_("core.blocks.help_text_embed_block"),
        ),
    )
    button_block = ButtonBlock()


class HeroBlock(StructBlock):
    background_image = ImageChooserBlock(required=False)
    background_color = CharBlock(required=False)
    foreground_color = CharBlock(required=False)
    pre_headline = CharBlock(required=False)
    headline = CharBlock(required=False)
    text = RichTextBlock(required=False, help_text=_("Inhalt"))
    link_text = CharBlock(
        required=True,
        default=_("Mehr erfahren"),
        help_text=_("Link Text, wird nur angezeigt wenn eine Seite oder ein"),
    )
    page = PageChooserBlock(
        required=False, help_text=_("Seite auf die verlinkt werden soll")
    )
    url = URLBlock(
        required=False, help_text=_("externe URL auf die verlinkt werden soll")
    )

    class Meta:
        icon = "image"
        template = "blocks/hero_block.html"
        label_format = _("Hero-Block")
        label = _("Hero-Block")

    def clean(self, value):
        result = super().clean(value)
        if result.get("page") and result.get("url"):
            raise ValidationError(
                _(
                    "Es kann nur entweder eine Seite oder eine externe URL verlinkt werden"
                )
            )
        return result

    def get_context(self, value: "ColumnHeroTextBlock", parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context.update(link=self.get_link(context))
        return context

    @staticmethod
    def get_link(context):
        if context.get("page", None):
            return context.get("page")
        if context.get("url", None):
            return context.get("url")
        return None


class VideoChooserBlock(DocumentChooserBlock):
    def __init__(self, accept=None, **kwargs):
        super().__init__(**kwargs)
        self.widget.attrs["accept"] = accept

    class Meta:
        template = "blocks/video_chooser_block.html"


"""
BaseStreamBlocks that are the base for the generic contentblocks
"""
