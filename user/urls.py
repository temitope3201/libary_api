
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', views.create_user, name='create-user'),
    path('list_all/', views.get_all_users, name='get-all-users'),
    path('user/<int:pk>/', views.user_detail, name='create-user'),
]