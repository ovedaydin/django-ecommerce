# Generated by Django 2.2.1 on 2021-04-13 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_customer_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='contact',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
