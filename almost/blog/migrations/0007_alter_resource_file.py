# Generated by Django 5.0.7 on 2024-07-19 03:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0006_delete_incident"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resource",
            name="file",
            field=models.FileField(upload_to="resource_files"),
        ),
    ]
