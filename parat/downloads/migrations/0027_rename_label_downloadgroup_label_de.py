# Generated by Django 4.1.13 on 2024-01-10 09:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("downloads", "0026_alter_downloadlanguage_label"),
    ]

    operations = [
        migrations.RenameField(
            model_name="downloadgroup",
            old_name="label",
            new_name="label_de",
        ),
    ]
