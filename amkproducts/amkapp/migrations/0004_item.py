# Generated by Django 2.2 on 2021-06-11 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amkapp', '0003_auto_20210611_1029'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
            ],
        ),
    ]
