# Generated by Django 2.2.1 on 2021-04-13 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_order_date_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='date_added',
        ),
        migrations.AddField(
            model_name='order',
            name='date_expected',
            field=models.DateField(blank=True, null=True),
        ),
    ]
