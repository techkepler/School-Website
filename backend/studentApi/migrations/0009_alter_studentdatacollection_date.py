# Generated by Django 4.1 on 2022-08-30 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("studentApi", "0008_studentdatacollection_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studentdatacollection",
            name="date",
            field=models.DateField(),
        ),
    ]