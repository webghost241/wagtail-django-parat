from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import (
    BooleanBlock,
    CharBlock,
    ChoiceBlock,
    IntegerBlock,
    ListBlock,
    PageChooserBlock,
    RichTextBlock,
    StructBlock,
    StructValue,
    TextBlock,
    URLBlock,
)

from .content_blocks import ImageBlock, ImageChooserBlock, VideoChooserBlock


class ColumnHeroTextBlock(StructBlock):
    pre_headline = CharBlock(required=False, label=_("Pre-Headline"))
    headline = TextBlock(required=True, label=_("Headline"))
    text = RichTextBlock(required=False, help_text=_("Inhalt"))
    link_text = CharBlock(
        required=False,
        help_text=_("Link Text, wird nur angezeigt wenn eine Seite oder ein"),
    )
    page = PageChooserBlock(
        required=False, help_text=_("Seite auf die verlinkt werden soll")
    )
    url = URLBlock(
        required=False, help_text=_("externe URL auf die verlinkt werden soll")
    )
    text_alignment = ChoiceBlock(
        choices=[("left", _("Linksbündig")), ("center", _("Zentriert"))],
        label=_("Textbündigkeit"),
        help_text=_("Textbündigkeit von Pre-Headline, Headline und Inhalt"),
        required=False,
    )

    class Meta:
        template = "blocks/column_hero_text_block.html"
        verbose_name = _("Hero-Spalten Text Block")
        label_format = _("Hero-Spalten Text Block")
        label = _("Hero-Spalten Text Block")

    def get_context(self, value: "ColumnHeroTextBlock", parent_context=None):
        column_size = parent_context.get("self").get("column_size")
        context = super().get_context(value, parent_context=parent_context)
        context.update(link=self.get_link(context), column_size=column_size)
        return context

    def clean(self, value):
        result = super().clean(value)
        if result.get("page") and result.get("url"):
            raise ValidationError(
                _(
                    "Es kann nur entweder eine Seite oder eine externe URL verlinkt werden"
                )
            )
        return result

    @staticmethod
    def get_link(context):
        if context.get("page", None):
            return context.get("page")
        if context.get("url", None):
            return context.get("url")
        return None


class ColumnHeroImageBlock(ImageBlock):
    image = ImageChooserBlock(required=True)
    aspect_ratio = ChoiceBlock(
        choices=[
            ("1-1", "1:1"),
            ("3-2", "3:2"),
        ],
        default="",
        required=False,
        label=_("Bildformat"),
    )

    class Meta:
        icon = "image"
        template = "blocks/colum_hero_image_block.html"
        label = _("Hero-Spalten Bild Block")
        label_format = _("Hero-Spalten Bild Block")


class ColumnHeroCarouselBlock(StructBlock):
    images = ListBlock(ImageChooserBlock(required=True))

    class Meta:
        icon = "image"
        template = "blocks/column_hero_carousel_block.html"
        label = _("Hero-Spalten Carousel Block")
        label_format = _("Hero-Spalten Carousel Block")


class HeadlineAndTextBlock(StructBlock):
    pre_headline = CharBlock(required=True, label=_("Pre-Headline"))
    headline = CharBlock(required=True, label=_("Headline"))
    text = RichTextBlock(required=True, help_text=_("Inhalt"))
    verbose_name = _("Hero-Spalten Text Block")
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
    centered = BooleanBlock(label=_("Zentrierter Text"), required=False)
    link_with_button = BooleanBlock(
        label=_("Buttonlink"),
        help_text=_(
            "Link wird als Button dargestellt.",
        ),
        required=False,
    )

    class Meta:
        label_format = _("Headline und Text Block")
        label = _("Headline und Text Block")
        template = "blocks/headline_and_text_block.html"

    def get_context(self, value: "ColumnHeroTextBlock", parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context.update(link=self.get_link(context))
        return context

    def clean(self, value):
        result = super().clean(value)
        if result.get("page") and result.get("url"):
            raise ValidationError(
                _(
                    "Es kann nur entweder eine Seite oder eine externe URL verlinkt werden"
                )
            )
        return result

    @staticmethod
    def get_link(context):
        if context.get("page", None):
            return context.get("page")
        if context.get("url", None):
            return context.get("url")
        return None


class HeadlineAndTextBlockWithVideo(HeadlineAndTextBlock):
    video = VideoChooserBlock(required=True)
    video_mobile = VideoChooserBlock(required=False)
    scroll_space = IntegerBlock(required=False)
    scroll_space_mobile = IntegerBlock(required=False)

    class Meta:
        label_format = _("Headline und Text Block Mit Video")
        label = _("Headline und Text Block Mit Video")
        template = "blocks/headline_and_text_block_with_video.html"


class DynamicChildrenCardsBlock(StructBlock):
    pre_headline = CharBlock(required=False, max_length=255)
    headline = CharBlock(required=False, max_length=255)
    link_text = CharBlock(max_length=255)

    class Meta:
        template = "blocks/dynamic_children_cards_block.html"


class VideoEmbedValue(StructValue):
    @property
    def video_url(self):
        url = self.get("url")
        local_video = self.get("local_video")
        return url if url else local_video.url

    @property
    def is_local_video(self):
        local_video = self.get("local_video")
        return local_video is not None


class VideoEmbedBlock(StructBlock):
    image = ImageChooserBlock(required=True, label=_("Vorschaubild"))
    aspect_ratio = ChoiceBlock(
        choices=[
            ("1-1", "1:1"),
            ("3-2", "3:2"),
        ],
        default="",
        required=False,
        label=_("Bildformat"),
    )
    url = URLBlock(
        required=False, label=_("Video URL"), help_text=_("Youtube oder Vimeo URL.")
    )
    local_video = VideoChooserBlock(
        required=False,
        label=_("Lokales Video"),
        help_text=_("Lokal gehostetes Video aussuchen"),
    )
    full_width = BooleanBlock(label=_("Ganze Breite"), required=False, default=False)
    auto_play = BooleanBlock(
        label=_("Auto Play"),
        help_text=_("Bestimmt ob das Video automatisch abgespielt werden soll."),
        required=False,
        default=True,
    )

    class Meta:
        icon = "image"
        template = "blocks/column_embed_block.html"
        label = _("Video Einbettungsblock")
        label_format = _("Video Einbettungsblock")
        value_class = VideoEmbedValue


class IconBlock(ImageBlock):
    image = ImageChooserBlock(required=True)
    pre_headline = CharBlock(required=False, max_length=255)
    headline = CharBlock(required=False, max_length=255)

    class Meta:
        icon = "image"
        template = "blocks/icon_block.html"
        label = _("Icon Block")
        label_format = _("Icon Block")
