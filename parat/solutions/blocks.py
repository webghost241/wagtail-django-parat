from django.utils.translation import gettext_lazy as _
from wagtail.blocks import CharBlock, ChoiceBlock, ListBlock, StructBlock
from wagtail.models import Locale

from parat.core.blocks import BaseLayoutBlock
from parat.core.blocks.content_blocks import (
    ImageBlock,
    ImageChooserBlock,
    VideoChooserBlock,
)


class DynamicSolutionBlock(BaseLayoutBlock):
    pre_headline = CharBlock(max_length=255)
    headline = CharBlock(max_length=255)
    link_text = CharBlock(max_length=255)

    class Meta:
        template = "blocks/dynamic_solutions_card_block.html"

    def get_context(self, value: "DynamicSolutionBlock", parent_context=None):
        context = super().get_context(value, parent_context)
        from parat.solutions.models import SolutionApplicationPage

        solutions = SolutionApplicationPage.objects.live().filter(
            locale=Locale.get_active()
        )
        context["self"].update(solutions=solutions)
        return context


class ImageSliderBlock(StructBlock):
    images = ListBlock(ImageChooserBlock(required=True))

    class Meta:
        icon = "image"
        template = "blocks/image_slider_block.html"
        label = _("Image Slider Block")
        label_format = _("Image Slider Block")


class ImageCollageBlock(StructBlock):
    images = ListBlock(ImageChooserBlock(required=True))
    style = ChoiceBlock(
        choices=[
            ("trinity", "Trinity"),
            ("waterfall", "Waterfall"),
        ],
        default="",
        required=False,
        label=_("Style"),
    )

    class Meta:
        icon = "image"
        template = "blocks/image_collage_block.html"
        label = _("Image Collage Block")
        label_format = _("Image Collage Block")
