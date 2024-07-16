# Generated by Django 4.1.13 on 2023-11-27 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("core", "0035_alter_dataprotectionpage_body_alter_homepage_body_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="standardpage",
            name="card_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="wagtailimages.image",
                verbose_name="Card Image",
            ),
        ),
    ]
