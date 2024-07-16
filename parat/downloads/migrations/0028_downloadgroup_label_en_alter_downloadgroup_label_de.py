# Generated by Django 4.1.13 on 2024-01-10 09:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("downloads", "0027_rename_label_downloadgroup_label_de"),
    ]

    operations = [
        migrations.AddField(
            model_name="downloadgroup",
            name="label_en",
            field=models.CharField(
                blank=True,
                max_length=255,
                null=True,
                unique=True,
                verbose_name="Label Englisch",
            ),
        ),
        migrations.AlterField(
            model_name="downloadgroup",
            name="label_de",
            field=models.CharField(
                max_length=255, unique=True, verbose_name="Label Deutsch"
            ),
        ),
    ]
