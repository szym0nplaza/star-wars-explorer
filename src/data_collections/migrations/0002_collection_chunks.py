# Generated by Django 4.1.6 on 2023-02-08 15:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data_collections", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="collection",
            name="chunks",
            field=models.IntegerField(default=1),
        ),
    ]
