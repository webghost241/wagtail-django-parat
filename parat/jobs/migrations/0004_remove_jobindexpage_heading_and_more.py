# Generated by Django 4.1.12 on 2023-10-19 11:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("jobs", "0003_jobindexpage"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="jobindexpage",
            name="heading",
        ),
        migrations.RemoveField(
            model_name="jobindexpage",
            name="subheading",
        ),
        migrations.AddField(
            model_name="jobindexpage",
            name="introduction",
            field=models.TextField(
                blank=True, help_text="core.models.standardpage_help_text_introduction"
            ),
        ),
    ]
