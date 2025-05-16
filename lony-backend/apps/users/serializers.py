from rest_framework import serializers
from .models import CustomUser
from .models import UserProfile
from django.contrib.auth.password_validation import validate_password

#Profile utilisateur
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'phone', 'bio']


#Mis à jour du profile 
class UserUpdateSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'profile']
        read_only_fields = ['id','first_name', 'email', 'role']  # le rôle ne devrait pas être modifiable ici

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        
        # Mise à jour des champs du CustomUser
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Mise à jour ou création du profil lié
        profile = getattr(instance, 'profile', None)
        if profile:
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance

# Liste utilisateur
class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'is_active', 'date_joined', 'role', 'profile']
        read_only_fields = ['id', 'is_active', 'date_joined','email', 'role']
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        
        # Mettre à jour les champs de CustomUser
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Mettre à jour UserProfile associé
        profile = instance.profile  # via related_name='profile' dans OneToOneField
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return instance


#Création utilisateurs
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'role']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


#Liste utilisateur
class UserListSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'profile']


#Modifier mot de pass user
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])