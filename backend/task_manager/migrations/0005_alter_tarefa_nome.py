# Generated by Django 4.2.5 on 2023-10-01 02:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("task_manager", "0004_tarefa_configuracoes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tarefa",
            name="nome",
            field=models.SlugField(max_length=40, unique=True),
        ),
    ]
