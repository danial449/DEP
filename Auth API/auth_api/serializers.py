from rest_framework import serializers
from auth_api.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
  # we are writing this because we need confirm password field in ur registration form
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = User
    fields = ['email' , 'name' , 'password', 'password2', 'tc']
    extra_kwargs = {
      'password':{'write_only':True}
    }

  #Validate Password and confirm password while registration
  def validate(self,attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    return attrs
  
  def create(self,validate_data):
    return User.objects.create_user(**validate_data)
  
class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id' , 'email' , 'name']