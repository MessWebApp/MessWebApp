# Generated by Django 3.2.6 on 2021-12-11 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messApp', '0007_auto_20211205_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='messdetails',
            name='extra_for_non_veg',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='messdetails',
            name='price_with_veg',
            field=models.IntegerField(default=0),
        ),
    ]
