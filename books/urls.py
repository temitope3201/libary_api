from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('list/', views.list_books, name='list-books'),
   path('add/', views.add_book, name='add-book'),
   path('borrow/<int:book_id>/', views.borrow_books, name='borrow-books'),
   path('return/<int:book_id>/', views.return_book, name='return-book'),
   path('available_books/', views.get_available_books, name = 'get-available-books'),
   path('user_borrowed_books/<int:user_id>/', views.get_borrowed_books, name='get-borrowed-books'),
   path('book_borrowers/<int:book_id>/', views.get_book_borrowers, name='get-book-borrowers'),
   path('book_detail/<int:book_id>/', views.get_book_detail, name='book-detail'),
   path('update_book/<int:book_id>/', views.update_delete_book, name = 'update-delete-book')

]