import uuid
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Season(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'season'

    def __str__(self):
        return '{}'.format(self.drama.title, self.cast.name)

class DramaSeason(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    season = models.ForeignKey('Season', null=True, blank=True, on_delete=models.CASCADE)
    drama = models.ForeignKey('Drama', null=True, blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'drama_seasons'

    def __str__(self):
        return '{}'.format(self.drama.title, self.season.name)
