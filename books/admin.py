from django.contrib import admin
from .models import Book, BookBorrow

# Register your models here.

admin.site.register(Book)
admin.site.register(BookBorrow)