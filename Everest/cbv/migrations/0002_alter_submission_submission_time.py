# Generated by Django 5.0.1 on 2024-02-08 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cbv", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="submission",
            name="submission_time",
            field=models.DateTimeField(null=True),
        ),
    ]
