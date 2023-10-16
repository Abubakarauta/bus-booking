from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .tokens import create_jwt_pair_for_user
from .models import Users
from .serializers import UserRegistrationSerialzer, UserProfileSerializer , UsersSerializer

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

class LogoutView(generics.GenericAPIView):
    """
    View to logout a user
    """
    queryset = Users.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = [UserProfileSerializer]

    def post(self, request):
        user = self.request.user
        try:
            refresh_token = request.data.get("refresh_token")
           
            token = RefreshToken(refresh_token)
            token.blacklist()

            serializer = UserProfileSerializer(user)
            response = {
                "message":"Successfully logged out.",
                "data": serializer.data
            } 
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
    
            response_data = {'error': 'Invalid refresh token'}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    queryset = Users.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UsersSerializer


    

class UserProfileView(generics.RetrieveAPIView):
    queryset= Users.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class= UserProfileSerializer

    def get_object(self):
        return self.request.user        