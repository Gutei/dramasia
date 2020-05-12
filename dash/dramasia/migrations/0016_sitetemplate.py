# Generated by Django 2.2.12 on 2020-04-22 22:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dramasia', '0015_auto_20200418_2116'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteTemplate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('code', models.CharField(default='-', max_length=128)),
                ('origin', models.CharField(default='-', max_length=128)),
                ('content', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'site_templates',
            },
        ),
    ]