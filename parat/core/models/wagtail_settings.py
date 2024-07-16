from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
)
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    BaseSiteSetting,
    register_setting,
)

@register_setting(icon="cr-google")
class AnalyticsSettings(BaseSiteSetting):
    class Meta:
        verbose_name = _("Tracking")

    ga_g_tracking_id = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_("G Tracking ID"),
        help_text=_('Ihre Google Analytics 4 tracking ID (beginnt mit "G-")')
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("ga_g_tracking_id")
            ],
            heading=_("Google Analytics"),
        )
    ]
