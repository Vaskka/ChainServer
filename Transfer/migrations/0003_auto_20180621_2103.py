# Generated by Django 2.0 on 2018-06-21 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Transfer', '0002_user_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
    ]