import datetime

from django.contrib.auth.models import AbstractBaseUser, UserManager, AbstractUser, PermissionsMixin
from django.db import models
from rest_framework.authtoken.models import Token as DefaultToken
from rest_framework import exceptions
from django.utils import timezone


# class AdminTokens(DefaultToken):
#     user = models.ForeignKey('Manager', related_name='auth_token', on_delete=models.CASCADE, )
#
#     def expired(self):
#         now = datetime.datetime.now(datetime.timezone.utc)
#         return now > self.created + datetime.timedelta(days=7)


class ParanoidQuerySet(models.QuerySet):
    """
    Prevents objects from being hard-deleted. Instead, sets the
    ``date_deleted``, effectively soft-deleting the object.
    """

    def delete(self):
        for obj in self:
            obj.deleted_status = True
            obj.deleted_at = timezone.now()
            obj.save()


class ParanoidManager(models.Manager):
    """
    Only exposes objects that have NOT been soft-deleted.
    """

    def get_queryset(self):
        return ParanoidQuerySet(self.model, using=self._db).filter(
            deleted_status=False)


class DefaultAbstract(models.Model):
    deleted_status = models.BooleanField(default=False, help_text='資料刪除狀態')
    created_at = models.DateTimeField(auto_now_add=True, help_text='建立時間')
    updated_at = models.DateTimeField(null=True, help_text='更新時間')
    deleted_at = models.DateTimeField(null=True, blank=True, help_text='刪除時間')
    objects = ParanoidManager()
    original_objects = models.Manager()

    class Meta:
        abstract = True
        # todo check 是否要updated_at
        # ordering = ['-updated_at', '-created_at']
        ordering = ['-created_at']

    def delete(self, **kwargs):
        self.deleted_status = True
        self.deleted_at = timezone.now()
        self.save()


class Word(DefaultAbstract):
    english = models.CharField(max_length=128, help_text='', null=True, unique=True)
    chinese = models.CharField(max_length=128, help_text='may many use,', null=True)
    word_type = models.CharField(max_length=128, help_text='', null=True)
    synonyms = models.ManyToManyField('Word', related_name='word_synonyms', help_text='同義詞')
    antonym = models.ManyToManyField('Word', related_name='word_antonym', help_text='反義詞')
    from_search = models.BooleanField(default=False)


class Explain(DefaultAbstract):
    word = models.ForeignKey(Word, related_name='explain', help_text='', on_delete=models.CASCADE)


class Sentence(DefaultAbstract):
    word = models.ForeignKey(Word, related_name='sentence', help_text='', on_delete=models.CASCADE)
    english = models.CharField(max_length=256, help_text='', null=True)
    chinese = models.CharField(max_length=256, help_text='may many use,', null=True)


class Exam(DefaultAbstract):
    pass


class Search(DefaultAbstract):
    pass
