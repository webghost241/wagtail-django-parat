from django.db import models
from wagtail.documents.models import Document, AbstractDocument


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class CustomDocument(AbstractDocument):
    # Custom field example:
    source = models.CharField(max_length=255, blank=True, null=True)

    admin_form_fields = Document.admin_form_fields + (
        # Add all custom fields names to make them appear in the form:
        "source",
    )

    def get_mb_file_size(self):
        file_size = self.get_file_size()
        if file_size:
            return round(file_size / (1024 * 1024), 2)
        return file_size
