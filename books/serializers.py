from rest_framework import serializers
from .models import Book, BookBorrow
from user.serializers import UserSerializer


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'

class BookBorrowSerializer(serializers.ModelSerializer):

    user = UserSerializer(required = False)
    book = BookSerializer(required = False)

    class Meta:

        model = BookBorrow
        fields = '__all__'


class BookUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'synopsis', 'total_copies']


