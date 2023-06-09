# Generated by Django 2.2.12 on 2020-04-09 06:19

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dramasia', '0005_drama_network'),
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'season',
            },
        ),
        migrations.CreateModel(
            name='DramaSeason',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('drama', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dramasia.Drama')),
                ('season', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dramasia.Season')),
            ],
            options={
                'db_table': 'drama_seasons',
            },
        ),
    ]
