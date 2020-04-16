# Generated by Django 2.2.12 on 2020-04-16 10:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dramasia', '0011_auto_20200416_0624'),
    ]

    operations = [
        migrations.CreateModel(
            name='MdlDrama',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('mdl_id', models.CharField(blank=True, max_length=128, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Sync from MDL',
                'db_table': 'mdl_drama',
            },
        ),
    ]
