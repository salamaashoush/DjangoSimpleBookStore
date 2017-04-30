from django.contrib import admin

# Register your models here.
from sarest.models import Book, Category, Reader ,Author

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Reader)
admin.site.register(Author)