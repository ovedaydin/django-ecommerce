# Generated by Django 2.2.1 on 2021-04-13 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_order_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='digital',
        ),
        migrations.AddField(
            model_name='order',
            name='shipping',
            field=models.BooleanField(default=True, null=True),
        ),
    ]