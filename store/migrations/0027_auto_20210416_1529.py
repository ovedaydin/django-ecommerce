# Generated by Django 2.2.1 on 2021-04-16 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0026_auto_20210416_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='contact',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
