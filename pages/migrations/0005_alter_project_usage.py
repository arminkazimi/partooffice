# Generated by Django 4.2.16 on 2025-01-24 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0004_alter_project_usage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project", name="usage", field=models.TextField(),
        ),
    ]
