# Generated by Django 4.2.5 on 2023-09-28 18:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("task_manager", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cliente",
            name="key",
            field=models.CharField(blank=True, max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name="parametro",
            name="data_atribuicao",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]