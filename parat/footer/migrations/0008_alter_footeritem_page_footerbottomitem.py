# Generated by Django 4.1.13 on 2024-01-10 08:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0083_workflowcontenttype"),
        ("footer", "0007_alter_footercolumn_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="footeritem",
            name="page",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="wagtailcore.page",
                verbose_name="Seite",
            ),
        ),
        migrations.CreateModel(
            name="FooterBottomItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "translation_key",
                    models.UUIDField(default=uuid.uuid4, editable=False),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=64, verbose_name="Titel")),
                ("url", models.URLField(blank=True, null=True, verbose_name="Url")),
                (
                    "icon_name",
                    models.CharField(
                        blank=True,
                        help_text="Bootstrap icon name",
                        max_length=32,
                        null=True,
                    ),
                ),
                (
                    "locale",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="wagtailcore.locale",
                    ),
                ),
                (
                    "page",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="wagtailcore.page",
                        verbose_name="Seite",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "unique_together": {("translation_key", "locale")},
            },
        ),
    ]
