from rest_framework import serializers
from .models import CustomUser, Role
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'firstname', 'lastname', 'email', 'is_superuser', 'date_joined', 'roles']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['firstname', 'lastname', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        firstname = validated_data.pop('firstname')
        lastname = validated_data.pop('lastname')

        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            firstname=firstname,
            lastname=lastname,
            password=password
        )

        # Assign only 'companion' and 'mentor' roles
        companion_role, _ = Role.objects.get_or_create(name='companion')
        mentor_role, _ = Role.objects.get_or_create(name='mentor')
        user.roles.add(companion_role, mentor_role)
        return user


class LoginSerializer(TokenObtainPairSerializer):
    role = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        role = attrs.get('role')

        if not email or not password or not role:
            raise serializers.ValidationError("Must include 'email', 'password', and 'role'.")

        user = authenticate(email=email, password=password)

        if user:
            if role == 'mentor' and user.roles.filter(name='mentor').exists():
                refresh = self.get_token(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': {
                        'email': user.email,
                        'firstname': user.firstname,
                        'lastname': user.lastname,
                        'is_superuser' : user.is_superuser,
                        'date_joined' : user.date_joined,
                        'role': 'mentor'
                    }
                }
                return data
            elif role == 'companion' and user.roles.filter(name='companion').exists():
                refresh = self.get_token(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': {
                        'email': user.email,
                        'firstname': user.firstname,
                        'lastname': user.lastname,
                        'is_superuser' : user.is_superuser,
                        'date_joined' : user.date_joined,
                        'role': 'companion'
                    }
                }
                update_last_login(None, user)

                return data
            else:
                raise serializers.ValidationError("Invalid role or unauthorized.")
        else:
            raise serializers.ValidationError("No active account found with the given credentials.")