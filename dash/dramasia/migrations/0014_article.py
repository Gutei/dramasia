# Generated by Django 2.2.12 on 2020-04-18 20:52

import ckeditor_uploader.fields
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dramasia', '0013_season_is_season'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='anime/image')),
                ('title', models.CharField(default='-', max_length=128)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('is_publish', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=512, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'articles',
            },
        ),
    ]
