# Generated by Django 5.0.6 on 2024-08-16 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0004_alter_variacao_preco_promocional'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variacao',
            name='preco_promocional',
            field=models.FloatField(null=True),
        ),
    ]
