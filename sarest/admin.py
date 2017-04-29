from django.contrib import admin

# Register your models here.
from sarest.models import Book, Category, Reader

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Reader)