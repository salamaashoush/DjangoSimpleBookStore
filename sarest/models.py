from django.db.models import Count
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
    value = models.PositiveSmallIntegerField(default=None)
    reed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

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
    models.ForeignKey(Author, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateField(null=True)
    cover = models.ImageField(upload_to='static/images', blank=True, null=True)
    category = models.ForeignKey('sarest.Category', related_name='books', on_delete=models.CASCADE, default=None)
    author = models.ForeignKey('sarest.Author', related_name='books', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

    @property
    def rating(self):
        rating_totals = self.reader_set.all().values('value').annotate(total=Count('id')).order_by('total')
        _total = 0
        _sum = 0
        _rating = 0
        for rating in rating_totals:
            _total = _total + rating.get('total')
            _sum = _sum + (rating.get('total') * rating.get('value'))

        if _total > 0:
            _rating = _sum / _total

        return ceil(_rating)
