# Generated by Django 4.1 on 2022-08-17 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("principal", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="estoqueproduto",
            name="data_lancamento",
            field=models.DateField(blank=True, null=True),
        ),
    ]
