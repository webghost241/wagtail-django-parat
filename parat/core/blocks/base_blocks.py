from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail import blocks


class AdvSettings(blocks.StructBlock):
    """
    Common fields each block should have,
    which are hidden under the block's "Advanced Settings" dropdown.
    """

    # placeholder, real value get set in __init__()
    custom_template = blocks.Block()

    custom_css_class = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Custom CSS Class"),
    )
    custom_id = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Custom ID"),
    )

    class Meta:
        form_template = "wagtailadmin/block_forms/base_block_settings_struct.html"
        label = _("Advanced Settings")

    def __init__(self, local_blocks=None, template_choices=None, **kwargs):
        if not local_blocks:
            local_blocks = ()

        local_blocks += (
            (
                "custom_template",
                blocks.ChoiceBlock(
                    choices=template_choices,
                    default=None,
                    required=False,
                    label=_("Template"),
                ),
            ),
        )


class AdvTrackingSettings(AdvSettings):
    """
    AdvSettings plus additional tracking fields.
    """

    ga_tracking_event_category = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Tracking Event Category"),
    )
    ga_tracking_event_label = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Tracking Event Label"),
    )


FRONTEND_COL_SIZE_CHOICES = [
    ("", "Always expanded"),
    ("sm", "sm - Expand on small screens (phone, 576px) and larger"),
    ("md", "md - Expand on medium screens (tablet, 768px) and larger"),
    ("lg", "lg - Expand on large screens (laptop, 992px) and larger"),
    ("xl", "xl - Expand on extra large screens (wide monitor, 1200px)"),
]
FRONTEND_COL_SIZE_DEFAULT = "md"


class AdvColumnSettings(AdvSettings):
    """
    BaseBlockSettings plus additional column fields.
    """

    column_breakpoint = blocks.ChoiceBlock(
        choices=FRONTEND_COL_SIZE_CHOICES,
        default=FRONTEND_COL_SIZE_CHOICES,
        required=False,
        verbose_name=_("Column Breakpoint"),
        help_text=_(
            "Screen size at which the column will expand horizontally or stack vertically."
        ),
    )


class BaseBlock(blocks.StructBlock):
    """
    Common attributes for all blocks used in Wagtail CRX.
    """

    # subclasses can override this to determine the advanced settings class
    advsettings_class = AdvSettings

    # placeholder, real value get set in __init__() from advsettings_class
    # settings = blocks.Block()

    def __init__(self, local_blocks=None, **kwargs):
        """
        Construct and inject settings block, then initialize normally.
        """
        klassname = self.__class__.__name__.lower()

        if not local_blocks:
            local_blocks = ()

        super().__init__(local_blocks, **kwargs)

    def render(self, value, context=None):
        # template = value["settings"]["custom_template"]

        template = self.get_template(context=context)
        if not template:
            return self.render_basic(value, context=context)

        if context is None:
            new_context = self.get_context(value)
        else:
            new_context = self.get_context(value, parent_context=dict(context))

        return mark_safe(render_to_string(template, new_context))


class BaseLayoutBlock(BaseBlock):
    """
    Common attributes for all blocks used in Wagtail CRX.
    """

    # Subclasses can override this to provide a default list of blocks for the content.
    content_streamblocks = []

    def __init__(self, local_blocks=None, **kwargs):
        if not local_blocks and self.content_streamblocks:
            local_blocks = self.content_streamblocks

        class ContentBlock(blocks.StreamBlock):
            class Meta:
                max_num = kwargs.get("max_num") if kwargs.get("max_num") else None
                min_num = kwargs.get("min_num") if kwargs.get("min_num") else None

        field_label = _(kwargs.get("label")) if kwargs.get("label") else _("Content")
        if local_blocks:
            local_blocks = (
                (
                    "content",
                    ContentBlock(local_blocks, label=field_label),
                ),
            )

        super().__init__(local_blocks, **kwargs)
