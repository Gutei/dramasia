import uuid
from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class ProfileUser(models.Model):

    MALE = 1
    FEMALE = 2

    GENDER = (
        (MALE, 'Laki-laki'),
        (FEMALE, 'Perempuan'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo_profile = models.ImageField(upload_to='user/profile', null=True, blank=True)
    biodata = models.TextField(null=True, blank=True)
    gender = models.PositiveIntegerField(choices=GENDER, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    website = models.CharField(max_length=512, null=True, blank=True)

    class Meta:
        db_table = 'user_profiles'

    def __str__(self):
        return '{}'.format(self.user.email)


class UserWatching(models.Model):
    WATCHING = 1
    FINISHED_WATCHING = 2
    HOLDING = 3
    STOP_WATCHING = 4

    STATE = (
        (WATCHING, 'Sedang ditonton'),
        (FINISHED_WATCHING, 'Selesai ditonton'),
        (HOLDING, 'Menunda'),
        (STOP_WATCHING, 'Tidak melanjutkan'),
    )

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('ProfileUser', null=True, blank=True, on_delete=models.CASCADE)
    drama = models.ForeignKey('Drama', null=True, blank=True, on_delete=models.CASCADE)
    status = models.PositiveIntegerField(choices=STATE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_watching'


class UserDramaScore(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('ProfileUser', null=True, blank=True, on_delete=models.CASCADE)
    drama = models.ForeignKey('Drama', null=True, blank=True, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_drama_scores'


class UserPolls(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('ProfileUser', null=True, blank=True, on_delete=models.CASCADE)
    drama = models.ForeignKey('Drama', null=True, blank=True, on_delete=models.CASCADE)
    poll = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_polls'
        verbose_name = 'Polling'


class UserDramaReview(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('ProfileUser', null=True, blank=True, on_delete=models.CASCADE)
    drama = models.ForeignKey('Drama', null=True, blank=True, on_delete=models.CASCADE)
    review = RichTextUploadingField(blank=True, null=True,)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_reviews'
        verbose_name = 'Review From User'


class UserMessage(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('ProfileUser', null=True, blank=True, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True,)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_messages'
        verbose_name = 'Pesan Untuk Developer'