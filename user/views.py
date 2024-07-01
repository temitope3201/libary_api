from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import UserSerializer, SignUpSerializer
from .models import User

# Create your views here.


@extend_schema(
    summary="Create User",
    description="Creating A Library User",
    request = SignUpSerializer,
    responses= SignUpSerializer,
    methods=['POST']
)
@permission_classes([AllowAny])
@api_view(['POST'])
def create_user(request):
    
    if request.method == 'POST':

        serializer = SignUpSerializer(data = request.data)
        if serializer.is_valid():
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            email = serializer.validated_data.get('email')
            phone_number = serializer.validated_data.get('phone_number')
            address = serializer.validated_data.get('address')

            if User.objects.filter(username = username).exists():
                return Response({'error': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                phone_number = phone_number,
                address = address
            )
            user.set_password(password)
            user.save()

            return Response({'message': 'User Creatted Successfully'}, status=status.HTTP_200_OK)
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@extend_schema(
    summary="List all Users",
    description="List all the users in the library",
    request=UserSerializer,
    methods=['GET']
)
@permission_classes([IsAuthenticated,IsAdminUser])
@api_view(['GET'])
def get_all_users(request):

    users = User.objects.all()

    serializer = UserSerializer(users, many = True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    summary='Get Update and Delete User Detail',
    description='Get, update, and delete the details of one User',
    request=UserSerializer,
    methods=['GET', 'PUT', 'DELETE']
)
@permission_classes([IsAuthenticated])
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, user_id):

    try:
        user = User.objects.get(id = user_id)

    except:
        return Response({"error": "User not found"}, status=status.HTTP_403_FORBIDDEN)
    

    current_user = request.user
    

    if current_user == user or current_user.isStaff == True:

        if request.method == 'GET': 

            serializer = UserSerializer(user)
            return Response(serializer.data, status= status.HTTP_200_OK)
        
        if request.method == 'PUT':

            serializer = UserSerializer(user, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if request.method == 'DELETE':

            user.delete()

            return Response({'message': 'User Deleted Successfully'}, status = status.HTTP_200_OK)
        

    return Response({'message':"You are not allowed to do this"}, status=status.HTTP_403_FORBIDDEN)



