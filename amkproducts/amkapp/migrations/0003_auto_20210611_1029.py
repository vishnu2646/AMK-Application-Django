# Generated by Django 2.2 on 2021-06-11 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amkapp', '0002_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, default='Ordered', max_length=100, null=True),
        ),
    ]
