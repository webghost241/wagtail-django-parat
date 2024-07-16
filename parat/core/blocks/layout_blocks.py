from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.blocks import StructBlock

from .base_blocks import AdvColumnSettings, BaseLayoutBlock


class ColumnBlock(BaseLayoutBlock):
    """
    Custom `StructBlock` that renders content in a column.
    """

    advsettings_class = AdvColumnSettings

    class Meta:
        template = "blocks/column_block.html"


class OriginalColumnBlock(BaseLayoutBlock):
    """
    Custom `StructBlock` that renders content in a column.
    """

    advsettings_class = AdvColumnSettings

    class Meta:
        template = "blocks/original_column_block.html"


class FullRowBlock(StructBlock):
    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(
            local_blocks=[
                (
                    "first",
                    ColumnBlock(local_blocks, max_num=1, min_num=1, label=_("Block")),
                ),
            ]
        )

    background_color = blocks.ChoiceBlock(
        choices=[
            ("", _("Default")),
            ("text-bg-dark", _("Schwarz")),
            ("text-bg-primary", _("Rot")),
            ("text-bg-light", _("Hellgrau")),
        ],
        default="",
        label=_("Hintergrundfarbe"),
        required=False,
    )

    class Meta:
        template = "blocks/full_row_block.html"
        label_format = _("Vollzeilenblock")
        label = _("Vollzeilenblock")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context["col_width_left"] = 12
        context["col_width_right"] = 0

        return context


class SplitRowBlock(StructBlock):
    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(
            local_blocks=[
                (
                    "first",
                    ColumnBlock(
                        local_blocks,
                        max_num=1,
                        min_num=1,
                        label=_("Linker Block"),
                    ),
                ),
                (
                    "second",
                    ColumnBlock(
                        local_blocks, max_num=1, min_num=1, label=_("Rechter Block")
                    ),
                ),
            ]
        )

    background_color = blocks.ChoiceBlock(
        choices=[
            ("", _("Default")),
            ("text-bg-dark", _("Schwarz")),
            ("text-bg-primary", _("Rot")),
            ("text-bg-light", _("Hellgrau")),
        ],
        default="",
        label=_("Hintergrundfarbe"),
        required=False,
    )

    column_size = blocks.ChoiceBlock(
        choices=[
            (6, _("Halb - 1/2 | 1/2 Spalten")),
            (4, _("Drittel - 1/3 | 2/3 Spalten")),
            (8, _("Drittel - 2/3 | 1/3 Spalten")),
        ],
        default=6,
        required=True,
        label=_("Spaltenaufteilung"),
    )
    mobile_ordering = blocks.ChoiceBlock(
        choices=[
            ("first", _("Erste über zweiter Spalte")),
            ("second", _("Zweite über erster Spalte")),
        ],
        default="first",
        required=True,
        label=_("Mobile Anordnung"),
        help_text=_(
            "Welche Spalte in der Mobilen Ansicht zuerst zu sehen sein soll."
            # todo tell if image should be first or second
        ),
    )

    class Meta:
        template = "blocks/row_block.html"
        label_format = _("Geteilter Zeilenblock")
        label = _("Geteilter Zeilenblock")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context["col_width_left"] = int(value["column_size"])
        context["col_width_right"] = 12 - int(value["column_size"])
        return context


class FourItemSplitRowBlock(StructBlock):
    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(
            local_blocks=[
                (
                    "first",
                    ColumnBlock(
                        local_blocks,
                        max_num=1,
                        min_num=1,
                        label=_("Erste Spalte"),
                    ),
                ),
                (
                    "second",
                    ColumnBlock(
                        local_blocks, max_num=1, min_num=1, label=_("Zweite Spalte")
                    ),
                ),
                (
                    "third",
                    ColumnBlock(
                        local_blocks, max_num=1, min_num=1, label=_("Dritte Spalte")
                    ),
                ),
                (
                    "fourth",
                    ColumnBlock(
                        local_blocks, max_num=1, min_num=1, label=_("Vierte Spalte")
                    ),
                ),
            ]
        )

    background_color = blocks.ChoiceBlock(
        choices=[
            ("", _("Default")),
            ("text-bg-dark", _("Schwarz")),
            ("text-bg-primary", _("Rot")),
            ("text-bg-light", _("Hellgrau")),
        ],
        default="",
        label=_("Hintergrundfarbe"),
        required=False,
    )

    class Meta:
        template = "blocks/four_item_column_row_block.html"
        label_format = _("4 Elemente Zeilenblock")
        label = _("4 Elemente Zeilenblock")


class ThreeItemSplitRowBlock(StructBlock):
    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(
            local_blocks=[
                (
                    "first",
                    ColumnBlock(
                        local_blocks,
                        max_num=1,
                        min_num=1,
                        label=_("Erste Spalte"),
                    ),
                ),
                (
                    "second",
                    ColumnBlock(
                        local_blocks, max_num=1, min_num=1, label=_("Zweite Spalte")
                    ),
                ),
                (
                    "third",
                    ColumnBlock(
                        local_blocks, max_num=1, min_num=1, label=_("Dritte Spalte")
                    ),
                ),
            ]
        )

    background_color = blocks.ChoiceBlock(
        choices=[
            ("", _("Default")),
            ("text-bg-dark", _("Schwarz")),
            ("text-bg-primary", _("Rot")),
            ("text-bg-light", _("Hellgrau")),
        ],
        default="",
        label=_("Hintergrundfarbe"),
        required=False,
    )

    class Meta:
        template = "blocks/three_item_column_row_block.html"
        label_format = _("3 Elemente Zeilenblock")
        label = _("3 Elemente Zeilenblock")
