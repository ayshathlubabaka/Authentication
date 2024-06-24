from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


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
        roles = validated_data.pop('roles', [])

        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            firstname=firstname,
            lastname=lastname,
            password=password,
        )
        for role in roles:
            user.roles.add(role)

        user.save()
        return user
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Convert the roles from a list of Role objects to a list of role names
        representation['roles'] = [role.name for role in instance.roles.all()]
        return representation

class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

class LoginSerializer(TokenObtainPairSerializer):
    role = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        role = attrs.get('role')

        if not email or not password or not role:
            raise serializers.ValidationError(_("Must include 'email', 'password', and 'role'."))

        user = authenticate(email=email, password=password)

        if user:
            if not user.is_registered or not user.is_verified:
                raise serializers.ValidationError(_("Account is not registered or verified."))

            if role == 'mentor' and user.roles.filter(name='mentor').exists():
                refresh = self.get_token(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': {
                        'email': user.email,
                        'firstname': user.firstname,
                        'lastname': user.lastname,
                        'is_superuser': user.is_superuser,
                        'date_joined': user.date_joined,
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
                        'is_superuser': user.is_superuser,
                        'date_joined': user.date_joined,
                        'role': 'companion'
                    }
                }
                update_last_login(None, user)
                return data
            elif role == 'hr' and user.roles.filter(name='hr').exists():
                refresh = self.get_token(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': {
                        'email': user.email,
                        'firstname': user.firstname,
                        'lastname': user.lastname,
                        'is_superuser': user.is_superuser,
                        'date_joined': user.date_joined,
                        'role': 'hr'
                    }
                }
                update_last_login(None, user)
                return data
            else:
                raise serializers.ValidationError(_("Invalid role or unauthorized."))
        else:
            raise serializers.ValidationError(_("No active account found with the given credentials."))