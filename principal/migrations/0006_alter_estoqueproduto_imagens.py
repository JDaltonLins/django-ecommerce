# Generated by Django 4.1 on 2022-08-20 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("principal", "0005_remove_estoqueproduto_custo_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="estoqueproduto",
            name="imagens",
            field=models.ManyToManyField(to="principal.estoqueprodutoimagem"),
        ),
    ]