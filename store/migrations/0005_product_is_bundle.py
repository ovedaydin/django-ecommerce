# Generated by Django 3.1.2 on 2021-02-22 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20210222_0132'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_bundle',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
