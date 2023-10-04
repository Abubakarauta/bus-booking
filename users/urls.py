from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import UserRegistrationAPIView, LogoutView, UserProfileView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name= 'user-registration'),
    path('token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name= 'token_verify'),
    path('logout/', LogoutView.as_view(), name= 'logout'),    
    path('profile/', UserProfileView.as_view(), name= 'profile'),
]