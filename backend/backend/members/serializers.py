from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(max_length=30)
    surnames = serializers.CharField(max_length=150)

    def create(self, validated_data):
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError("El email ya existe en la base de datos")
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            surnames=validated_data['surnames']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)  


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'surnames']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'name', 'surnames', 'birthdate', 'addressLetters',
            'phoneNumber', 'bankAccount', 'languageConf', 
            'documentID', 'documentType', 'contactIsPublic'
        ]