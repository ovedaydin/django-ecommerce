# Generated by Django 2.2.1 on 2021-04-13 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_auto_20210413_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='address1',
            field=models.CharField(default='empty', max_length=200),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='address2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='city',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='company',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='contact',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='district',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='phone',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='postcode',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='surname',
            field=models.CharField(max_length=200),
        ),
    ]
