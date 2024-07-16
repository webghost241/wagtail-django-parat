# Generated by Django 4.1.13 on 2023-12-13 13:52

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("wagtailcore", "0083_workflowcontenttype"),
        ("core", "0046_auto_20231213_1352"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customflatmenu",
            name="locale",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="wagtailcore.locale",
            ),
        ),
        migrations.AlterField(
            model_name="customflatmenu",
            name="translation_key",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name="customflatmenuitem",
            name="locale",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="wagtailcore.locale",
            ),
        ),
        migrations.AlterField(
            model_name="customflatmenuitem",
            name="translation_key",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterUniqueTogether(
            name="customflatmenu",
            unique_together={("translation_key", "locale")},
        ),
        migrations.AlterUniqueTogether(
            name="customflatmenuitem",
            unique_together={("translation_key", "locale")},
        ),
    ]
