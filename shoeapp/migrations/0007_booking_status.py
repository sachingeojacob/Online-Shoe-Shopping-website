# Generated by Django 3.0.7 on 2020-06-21 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoeapp', '0006_product_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(default='Packing', max_length=50),
        ),
    ]
