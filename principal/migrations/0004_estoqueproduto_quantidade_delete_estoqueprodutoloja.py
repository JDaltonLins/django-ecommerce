# Generated by Django 4.1 on 2022-08-19 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("principal", "0003_alter_estoqueproduto_data_lancamento"),
    ]

    operations = [
        migrations.AddField(
            model_name="estoqueproduto",
            name="quantidade",
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name="EstoqueProdutoLoja",
        ),
    ]