# Generated by Django 4.1 on 2022-09-16 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teacherApi", "0005_homeworkmodel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homeworkmodel",
            name="date",
            field=models.DateField(),
        ),
    ]