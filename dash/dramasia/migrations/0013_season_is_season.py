# Generated by Django 2.2.12 on 2020-04-17 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dramasia', '0012_mdldrama'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='is_season',
            field=models.BooleanField(default=False, verbose_name='This season'),
        ),
    ]
