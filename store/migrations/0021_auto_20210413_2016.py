# Generated by Django 2.2.1 on 2021-04-13 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_shippingaddress_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='address2',
            field=models.CharField(default=' ', max_length=200, null=True),
        ),
    ]
