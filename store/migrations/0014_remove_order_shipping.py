# Generated by Django 2.2.1 on 2021-04-13 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_auto_20210413_1419'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shipping',
        ),
    ]
