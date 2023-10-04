from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model, authenticate
from .models import Users

User = get_user_model() 

class UserRegistrationSerialzer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, required = True, style = { 'input':'password' } )


    class Meta:
        model = Users
        fields = ['email','password', 'username','first_name','last_name']

    def create(self, validated_data):
        user =Users(
            email = validated_data['email'],
            first_name =validated_data['first_name'],
            last_name = validated_data['last_name'],
            username = validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.is_active=True
        user.save()
        return user
    
    def validate_if_user_exists(self, attrs):
        if User.objects.filter(email=attrs).exists():
            raise serializers.ValidationError("this email already exists")
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'username', 'phone_number']



#class UserAuthenticationSerializer(TokenObtainPairView):

 #   email = serializers.EmailField()
  #  password = serializers.CharField(write_only = True, required = True, style = { 'input':'password '})
   # 
    #def validate(self, data):
     #   email = data.get('email')
      #  password =data.get('password')
#
 #       user = authenticate(username = email , password= password)
#
 #       if not user:
  #          raise serializers.ValidationError('invalid Credentials')
   ##        raise serializers.ValidationError('User account is disable')
     #   return user
