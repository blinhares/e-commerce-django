# Generated by Django 5.0.6 on 2024-08-16 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0003_variacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variacao',
            name='preco_promocional',
            field=models.FloatField(default=0, null=True),
        ),
    ]
