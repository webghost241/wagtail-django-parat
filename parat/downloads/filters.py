from django.utils.translation import gettext_lazy as _
from django_filters import filters, FilterSet

from parat.downloads.models import Download, DownloadGroup, DownloadLanguage


class DownloadFilter(FilterSet):
    c = filters.ModelChoiceFilter(
        queryset=DownloadGroup.objects.all(),
        method="category_filter",
        empty_label=_("Alle Kategorien"),
    )
    l = filters.ModelChoiceFilter(
        queryset=DownloadLanguage.objects.all(),
        method="language_filter",
        empty_label=_("Alle Sprachen"),
    )

    class Meta:
        Model = Download
        fields = ["c", "l"]

    @staticmethod
    def category_filter(queryset, name, value):
        return queryset.filter(
            **{
                "download_group": value,
            }
        )

    @staticmethod
    def language_filter(queryset, name, value):
        return queryset.filter(
            **{
                "download_languages": value,
            }
        )
