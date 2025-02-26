# Generated by Django 4.1.12 on 2023-10-17 09:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import functools
import parat.core.util.fileutil
import wagtail.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("wagtailcore", "0083_workflowcontenttype"),
    ]

    operations = [
        migrations.CreateModel(
            name="JobPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("headline", models.CharField(max_length=255)),
                ("text", wagtail.fields.RichTextField()),
                (
                    "file",
                    models.FileField(
                        upload_to=functools.partial(
                            parat.core.util.fileutil.upload_generic_namer,
                            *("jobs/",),
                            **{}
                        ),
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["pdf"]
                            )
                        ],
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]
