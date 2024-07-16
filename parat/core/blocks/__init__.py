from typing import List, Tuple

import wagtail.blocks
from django.utils.translation import gettext_lazy as _
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock

from .content_blocks import BaseStreamBlock, ButtonBlock, HeroBlock, ImageBlock
from .layout_blocks import (
    BaseLayoutBlock,
    FourItemSplitRowBlock,
    FullRowBlock,
    SplitRowBlock,
    ThreeItemSplitRowBlock,
)
from .parat_blocks import (
    ColumnHeroCarouselBlock,
    ColumnHeroImageBlock,
    ColumnHeroTextBlock,
    HeadlineAndTextBlock,
    IconBlock,
    VideoEmbedBlock,
)

HTML_STREAMBLOCKS = [
    ("text", wagtail.blocks.RichTextBlock()),
    ("image", ImageBlock()),
]

CONTENT_STREAMBLOCKS = HTML_STREAMBLOCKS + []

LAYOUT_STREAMBLOCKS = [
    ("row", SplitRowBlock(CONTENT_STREAMBLOCKS)),
]

COLUMN_HERO_STREAMBLOCKS = [
    (
        "row",
        SplitRowBlock(
            [
                ("image", ColumnHeroImageBlock()),
                ("carousel", ColumnHeroCarouselBlock()),
                ("text", ColumnHeroTextBlock()),
            ]
        ),
    ),
]
COLUMN_HERO_ALTERNATE_STREAMBLOCKS = [
    (
        "split_row_block",
        SplitRowBlock(
            [
                ("image", ColumnHeroImageBlock()),
                ("carousel", ColumnHeroCarouselBlock()),
                ("text", ColumnHeroTextBlock()),
                ("video_embed_block", VideoEmbedBlock()),
                ("icon_block", IconBlock()),
            ]
        ),
    ),
    (
        "full_row_block",
        FullRowBlock(
            [
                ("image", ColumnHeroImageBlock()),
                ("text", ColumnHeroTextBlock()),
                ("video_embed_block", VideoEmbedBlock()),
                ("icon_block", IconBlock()),
            ],
        ),
    ),
    (
        "four_item_split_row_block",
        FourItemSplitRowBlock(
            [
                ("image", ColumnHeroImageBlock()),
                ("carousel", ColumnHeroCarouselBlock()),
                ("text", ColumnHeroTextBlock()),
                ("video_embed_block", VideoEmbedBlock()),
                ("icon_block", IconBlock()),
            ]
        ),
    ),
    (
        "three_item_split_row_block",
        ThreeItemSplitRowBlock(
            [
                ("image", ColumnHeroImageBlock()),
                ("carousel", ColumnHeroCarouselBlock()),
                ("text", ColumnHeroTextBlock()),
                ("video_embed_block", VideoEmbedBlock()),
                ("icon_block", IconBlock()),
            ]
        ),
    ),
]

BASE_STREAM_BLOCKS = [
    *COLUMN_HERO_ALTERNATE_STREAMBLOCKS,
    ("paragraph_block", wagtail.blocks.RichTextBlock(icon="pilcrow")),
    ("headline_and_text_block", HeadlineAndTextBlock()),
    ("image_block", ImageBlock()),
    ("block_quote", wagtail.blocks.BlockQuoteBlock()),
    (
        "embed_block",
        EmbedBlock(
            help_text=_("core.blocks.help_text_embed_block"),
        ),
    ),
    ("button_block", ButtonBlock()),
    ("video_embed_block", VideoEmbedBlock()),
    ("icon_block", IconBlock()),
]

"""
The blocks that are used for heroblock components
"""
BASE_HERO_BLOCKS = [
    ("background_image", ImageChooserBlock(required=False)),
    ("background_color", wagtail.blocks.CharBlock(required=False)),
    (
        "foreground_color",
        wagtail.blocks.CharBlock(required=False),
    ),
]


class ContentFieldFactory:
    extra_blocks = []
    include_hero_block = True

    def set_extra_blocks(self, extra_blocks: List[Tuple[str, wagtail.blocks.Block]]):
        self.extra_blocks = extra_blocks
        return self

    def set_include_her_block(self, value: bool):
        """
        Used to disalbe the hero block
        """
        self.include_hero_block = value
        return self

    def __get_general_stream_blocks(self) -> List[Tuple[str, wagtail.blocks.Block]]:
        """
        Internal method to create the base block
        """
        return [*BASE_STREAM_BLOCKS] + self.extra_blocks

    def __get_hero_block(self) -> wagtail.blocks.StructBlock:
        """
        Method that returns a hero block, a mix of a general stream block with extra struct items.
        """
        return HeroBlock()

    def get_general_body(self) -> StreamField:
        """
        Method to provide the general body to a page. Is the baseline for all pages and can be adapted by adding extra blocks
        for an example see JobIndexPage
        """
        stream_fields = [
            *self.__get_general_stream_blocks(),
        ]
        if self.include_hero_block:
            stream_fields.append(("hero", self.__get_hero_block()))
        return StreamField(
            stream_fields,
            verbose_name=_("Seiten Inhalt"),
            blank=True,
            collapsed=True,
            use_json_field=True,
        )
