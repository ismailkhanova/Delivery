# Generated by Django 3.0.11 on 2020-11-22 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='available',
            field=models.BooleanField(default=True, verbose_name='Доступен'),
        ),
    ]
