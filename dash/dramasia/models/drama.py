import uuid
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.template.defaultfilters import slugify

class Drama(models.Model):

    TV = 1
    MOVIE = 2

    TYPE = (
        (TV, 'TV'),
        (MOVIE, 'Movie')
    )

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    mdl_id = models.CharField(max_length=256, null=True, blank=True)
    image = models.ImageField(upload_to='drama/image', null=True, blank=True, max_length=1500)
    image_url = models.CharField(null=True, blank=True, max_length=1500)
    image_binary = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=128, default="-")
    native_title = models.CharField(max_length=128, null=True, blank=True)
    english_title = models.CharField(max_length=128, null=True, blank=True)
    alias = models.TextField(null=True, blank=True)
    type = models.PositiveIntegerField(choices=TYPE, null=True, blank=True )
    description = RichTextUploadingField(blank=True, null=True, extra_plugins=['uploadimage'],)
    airing_date = models.CharField(max_length=128, null=True, blank=True)
    rating = models.CharField(max_length=128, null=True, blank=True)
    mdl_score = models.DecimalField(default=0, max_digits=4, decimal_places=1)
    network = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=128, null=True, blank=True)
    website = models.TextField(null=True, blank=True)
    total_episode = models.PositiveIntegerField(default=0)
    duration = models.CharField(max_length=128, null=True, blank=True)
    slug = models.SlugField(max_length=512, blank=True, null=True,)
    is_publish = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dramas'

    def __str__(self):
        return '{}'.format(self.title)

    def save(self, *args, **kwargs):
        uid = self.id.hex[:4]

        self.slug = '{}-{}'.format(uid, slugify(self.title))

        super(Drama, self).save(*args, **kwargs)

class DramaTag(models.Model):

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    drama = models.ForeignKey('Drama', null=True, blank=True, on_delete=models.CASCADE)
    tag = models.CharField(max_length=256, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'drama_tags'

    def __str__(self):
        return '{} - {}'.format(self.drama.title, self.tag)

class Genre(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    genre = models.CharField(max_length=256, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'genres'

    def __str__(self):
        return '{}'.format(self.genre)


class DramaGenre(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    drama = models.ForeignKey('Drama', null=True, blank=True, on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', null=True, blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'drama_genres'

    def __str__(self):
        return '{}'.format(self.drama.title, self.genre.genre)


class Cast(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256, null=True, blank=True)
    image = models.ImageField(upload_to='drama/image', null=True, blank=True, max_length=1500)
    image_url = models.CharField(null=True, blank=True, max_length=1500)
    image_binary = models.TextField(null=True, blank=True)
    id_ime = models.CharField(max_length=256, null=True, blank=True)
    birth_date = models.DateTimeField(null=True, blank=True)
    biodata = RichTextUploadingField(blank=True, null=True, extra_plugins=['uploadimage'],)
    slug = models.SlugField(max_length=512, blank=True, null=True,)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'casts'

    def __str__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        uid = self.id.hex[:4]

        self.slug = '{}-{}'.format(uid, slugify(self.name))

        super(Cast, self).save(*args, **kwargs)


class DramaCast(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    drama = models.ForeignKey('Drama', null=True, blank=True, on_delete=models.CASCADE)
    cast = models.ForeignKey('Cast', null=True, blank=True, on_delete=models.CASCADE)
    role = models.CharField(max_length=128, null=True, blank=True)
    cast_as = models.CharField(max_length=256, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'drama_casts'

    def __str__(self):
        return '{}'.format(self.drama.title, self.cast.name)