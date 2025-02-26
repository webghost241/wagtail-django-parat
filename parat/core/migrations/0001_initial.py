# Generated by Django 4.1.11 on 2023-09-06 10:43

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.blocks
import wagtail.contrib.forms.models
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("wagtailcore", "0083_workflowcontenttype"),
    ]

    operations = [
        migrations.CreateModel(
            name="FormPage",
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
                (
                    "to_address",
                    models.CharField(
                        blank=True,
                        help_text="Optional - form submissions will be emailed to these addresses. Separate multiple addresses by comma.",
                        max_length=255,
                        validators=[wagtail.contrib.forms.models.validate_to_address],
                        verbose_name="to address",
                    ),
                ),
                (
                    "from_address",
                    models.EmailField(
                        blank=True, max_length=255, verbose_name="from address"
                    ),
                ),
                (
                    "subject",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="subject"
                    ),
                ),
                ("intro", wagtail.fields.RichTextField(blank=True)),
                ("thank_you_text", wagtail.fields.RichTextField(blank=True)),
            ],
            options={
                "abstract": False,
            },
            bases=(
                wagtail.contrib.forms.models.FormMixin,
                "wagtailcore.page",
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="StandardPage",
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
                (
                    "introduction",
                    models.TextField(
                        blank=True,
                        help_text="core.models.standardpage_help_text_introduction",
                    ),
                ),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            (
                                "paragraph_block",
                                wagtail.blocks.RichTextBlock(icon="pilcrow"),
                            ),
                            (
                                "image_block",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "image",
                                            wagtail.images.blocks.ImageChooserBlock(
                                                required=True
                                            ),
                                        ),
                                        (
                                            "caption",
                                            wagtail.blocks.CharBlock(required=False),
                                        ),
                                        (
                                            "attribution",
                                            wagtail.blocks.CharBlock(required=False),
                                        ),
                                    ]
                                ),
                            ),
                            ("block_quote", wagtail.blocks.BlockQuoteBlock()),
                            (
                                "embed_block",
                                wagtail.embeds.blocks.EmbedBlock(
                                    help_text="core.blocks.help_text_embed_block"
                                ),
                            ),
                        ],
                        blank=True,
                        use_json_field=True,
                        verbose_name="core.models.standardpage_verbose_name_body",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="FormField",
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
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "clean_name",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="Safe name of the form field, the label converted to ascii_snake_case",
                        max_length=255,
                        verbose_name="name",
                    ),
                ),
                (
                    "label",
                    models.CharField(
                        help_text="The label of the form field",
                        max_length=255,
                        verbose_name="label",
                    ),
                ),
                (
                    "field_type",
                    models.CharField(
                        choices=[
                            ("singleline", "Single line text"),
                            ("multiline", "Multi-line text"),
                            ("email", "Email"),
                            ("number", "Number"),
                            ("url", "URL"),
                            ("checkbox", "Checkbox"),
                            ("checkboxes", "Checkboxes"),
                            ("dropdown", "Drop down"),
                            ("multiselect", "Multiple select"),
                            ("radio", "Radio buttons"),
                            ("date", "Date"),
                            ("datetime", "Date/time"),
                            ("hidden", "Hidden field"),
                        ],
                        max_length=16,
                        verbose_name="field type",
                    ),
                ),
                (
                    "required",
                    models.BooleanField(default=True, verbose_name="required"),
                ),
                (
                    "choices",
                    models.TextField(
                        blank=True,
                        help_text="Comma or new line separated list of choices. Only applicable in checkboxes, radio and dropdown.",
                        verbose_name="choices",
                    ),
                ),
                (
                    "default_value",
                    models.TextField(
                        blank=True,
                        help_text="Default value. Comma or new line separated values supported for checkboxes.",
                        verbose_name="default value",
                    ),
                ),
                (
                    "help_text",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="help text"
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="form_fields",
                        to="core.formpage",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
        ),
    ]
