# Generated by Django 3.1.5 on 2021-01-16 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20210116_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='金额'),
        ),
    ]