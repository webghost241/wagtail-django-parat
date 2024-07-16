from django.utils.translation import gettext_lazy as _
from django_filters import filters, FilterSet

from parat.expo.models import Expo, ExpoCategory


class ExpoFilter(FilterSet):
    c = filters.ModelChoiceFilter(
        queryset=ExpoCategory.objects.all(),
        method="category_filter",
        empty_label=_("Alle Kategorien"),
    )

    class Meta:
        Model = Expo
        fields = ["c"]

    def category_filter(self, queryset, name, value):
        return queryset.filter(
            **{
                "categories": value,
            }
        )
