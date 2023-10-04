from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .tokens import create_jwt_pair_for_user
from .models import Users
from .serializers import UserRegistrationSerialzer, UserProfileSerializer

class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerialzer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = UserRegistrationSerialzer(data= request.data)

        if serializer.is_valid():
            serializer.save()
            response = {
                'message':'user created successfully',
                'first_name':serializer.data['first_name'],
                'last_name': serializer.data['last_name'],
                'email': serializer.data['email'],

            }

            return Response(response, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            # Blacklist the refresh token to prevent further use (optional)
            refresh_token = RefreshToken(request.data.get('refresh_token'))
            refresh_token.blacklist()

            # Here, you can perform any additional actions related to "logging out"
            # For example, you might want to clear any session data or perform other cleanup operations.
            # This will depend on your specific bus booking application's requirements.

            response_data = {'message': 'User logout successfully'}
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {'error': 'Invalid refresh token'}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)






    

class UserProfileView(generics.RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class= UserProfileSerializer

    def get_object(self):
        return self.request.user        