from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import BookSerializer, BookBorrowSerializer, BookUpdateSerializer
from .models import Book, BookBorrow
from django.contrib.auth import get_user_model,get_user


User = get_user_model()

# Create your views here.

@extend_schema(
    summary='List All Books',
    description='List all the books present in the Library',
    request=BookSerializer,
    responses=BookSerializer,
    methods=['GET']
)
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def list_books(request):

    books = Book.objects.all()

    serializer = BookSerializer(books, many = True)

    return Response(serializer.data, status = status.HTTP_200_OK)

@extend_schema(
    summary='Add Book',
    description='Add A Book To The Library',
    request=BookSerializer,
    responses=BookBorrowSerializer,
    methods=['POST']
)
@permission_classes([IsAdminUser])
@api_view(['POST'])
def add_book(request):

    serializer = BookSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save()

        return Response({'message':'Book Added Successfully'}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary='Borrow A Book',
    description='View To Borrow a book from the library',
    request=BookBorrowSerializer,
    responses=BookBorrowSerializer,
    methods=['POST']
)
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def borrow_books(request, book_id):


    

    book = Book.objects.get(book_id)

    if book.available_copies >= 1:

        book.available_copies -=1

        book.save()

        borrowed_book = BookBorrow.objects.create(user = request.user, book = book)
        borrowed_book.save()

        serializer = BookBorrowSerializer(borrowed_book)

        return Response(serializer.data, status=status.HTTP_200_OK)



    else:
        return Response({'error': 'Book is not available'}, status=status.HTTP_404_NOT_FOUND)
    

@extend_schema(
    summary='Return A Book',
    description='View To Return A Book',
    methods=['DELETE'],
)
@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def return_book(request, book_id):

    book = Book.objects.get(book_id)

    book.available_copies += 1
    book.save()

    returning_book = BookBorrow.objects.filter(book = book, user = request.user)

    if returning_book is not None:

        returning_book.delete()

        return Response({'message': 'Book Returned Successfully'}, status=status.HTTP_200_OK)
    
    else:
        return Response({'error': 'This book was not borrowed by this user'}, status=status.HTTP_400_BAD_REQUEST)
    
@extend_schema(
    summary='Filter Available Books',
    description='View To view available books',
    methods=['GET'],
    request=BookSerializer,
    responses=BookSerializer,
)
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_available_books(request):

    available_books = Book.objects.filter(available_copies_gt=0)

    serializer = BookSerializer(available_books, many = True)

    return Response(serializer.data, status=status.HTTP_200_OK)



@extend_schema(
    summary='Get Borrowed Books',
    description='Get the books borrowed by a User',
    methods=['GET'],
    responses=BookBorrowSerializer
)
@permission_classes([IsAuthenticated,IsAdminUser])
@api_view(['GET'])
def get_borrowed_books(request,user_id):

    book_user = User.objects.get(id=user_id)
    current_user = get_user(request)

    if current_user.is_staff or book_user == current_user:

        borrowed_books = BookBorrow.objects.filter(user = book_user)
        serializer = BookBorrowSerializer(borrowed_books, many = True)

        return Response(serializer.data, status = status.HTTP_200_OK)
    
    else:
        return Response({'error': 'You are not permitted to view this'}, status=status.HTTP_403_FORBIDDEN)
    

@extend_schema(
    summary='Get Book Borrowers',
    description='Get the Users that borrowed a book',
    methods=['GET'],
    responses=BookBorrowSerializer
)
@permission_classes([IsAdminUser])
@api_view(['GET'])
def get_book_borrowers(request,book_id):

    borrowed_book = Book.objects.get(id = book_id)

    book_borrowers = BookBorrow.objects.filter(book = borrowed_book)

    serializer = BookBorrowSerializer(book_borrowers, many = True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    summary='Get Book Detail',
    description='Get The detail of a particular book',
    methods=['GET'],
    responses=BookSerializer
)
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_book_detail(request, book_id):

    book = Book.objects.get(id=book_id)
    serializer = BookSerializer(book)

    return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    summary='Update and Delete Book',
    description='Update and Delete the details of a book',
    methods=['GET', 'PUT'],
    responses= BookUpdateSerializer,
    request=BookUpdateSerializer
)
@permission_classes([IsAdminUser])
@api_view(['PUT','DELETE'])
def update_delete_book(request, book_id):

    book = Book.objects.get(id = book_id)

    if book is not None:
    
        if request.method == 'PUT':

            serializer = BookUpdateSerializer(book, data=request.data)

            if serializer.is_valid:
                serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)
            
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        if request.method == 'DELETE':

            book.objects.delete()

            return Response({'message': 'Book Deleted Successfully'}, status = status.HTTP_200_OK)
        
    return Response({"error": "Book not found"}, status=status.HTTP_403_FORBIDDEN)


