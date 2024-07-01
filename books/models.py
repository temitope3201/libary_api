from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Book(models.Model):

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    synopsis = models.TextField()
    genre = models.CharField(max_length=100)
    total_copies = models.IntegerField()
    available_copies = models.IntegerField()

    def __str__(self):
        return f'{self.title} by {self.author}'
    
class BookBorrow(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    time_borrowed = models.DateTimeField(auto_now_add=True)
   

    def __str__(self):

        return f'{self.book} borrowed by {self.user}'


    


