from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Count, Avg
from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from math import ceil


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    subscribers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name


class Reader(models.Model):
    user = models.ForeignKey('auth.User', related_name='user', on_delete=models.CASCADE, default=None)
    book = models.ForeignKey('sarest.Book', related_name='book', on_delete=models.CASCADE, default=None)
    value = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    reed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book',)

    def __str__(self):
        return self.user.username + ' : ' + self.book.title


class Author(models.Model):
    name = models.CharField(max_length=100)
    born_at = models.DateField(null=True)
    died_at = models.DateField(null=True)
    website = models.CharField(null=True, max_length=100)
    bio = models.TextField(null=True)
    image = models.ImageField(upload_to='static/images', blank=True, null=True)
    followers = models.ManyToManyField(User, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateField(null=True)
    cover = models.ImageField(upload_to='static/images', blank=True, null=True)
    category = models.ForeignKey('sarest.Category', related_name='books', on_delete=models.CASCADE, default=None)
    author = models.ForeignKey('sarest.Author', related_name='books', on_delete=models.CASCADE, default=None)
    readers = models.ManyToManyField(User, through=u'Reader', related_name=u'readers')

    def __str__(self):
        return self.title
