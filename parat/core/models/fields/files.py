from django.db import models

from parat.core.forms.fields import SVGAndImageFormField


class SVGAndImageField(models.ImageField):
    def formfield(self, **kwargs):
        defaults = {"form_class": SVGAndImageFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
