# Generated by Django 4.1.7 on 2023-04-03 00:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantes', '0006_userplante_date_futur_alter_rappel_emaildate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rappel',
            name='emailDate',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
