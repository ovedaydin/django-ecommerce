# Generated by Django 2.2.1 on 2021-04-13 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_order_takeaway'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='address',
            new_name='address1',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='zipcode',
            new_name='postcode',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='state',
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='address2',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='company',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='contact',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='district',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='phone',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='surname',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
