from rest_framework import serializers 
from django.contrib.auth import get_user_model, authenticate
from books.models import Book


User = get_user_model()
  
class SignUpSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length = 100)
    last_name = serializers.CharField(max_length = 100)
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length = 200)

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'address']


