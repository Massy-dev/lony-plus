from django.shortcuts import render
from .models import *
from .permissions import *
from rest_framework import generics, permissions, status
from .serializers import *
from rest_framework.permissions import AllowAny,IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

#Créer un utilisateur
class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

# Recuperation et modifiction du profil utilisateur
class UserProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwner]

    def get_object(self):
        # Récupère le profil de l’utilisateur connecté
        return self.request.user.profile
# Create your views here.


# Deconnexion utilisateur
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request):
        print("bing")
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Déconnexion réussie."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            raise ValidationError({"error": "Token invalide ou déjà blacklisté."})
    

#View profil utilisateur
class UserMeView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get detail user
class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'  # permet d'accéder via /api/users/<id>/


#Supression de profil utilisateur
class UserDeleteView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwner]

    def get_queryset(self):
        """
        Ne permettre à un utilisateur de supprimer QUE son propre compte.
        (Un admin pourrait avoir une autre vue spéciale plus tard)
        """
        user = self.request.user
        return CustomUser.objects.filter(id=user.id)

# Supression par l'admin
class UserByAdminDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, pk, format=None):
        user = get_object_or_404(CustomUser, pk=pk)
        user.delete()
        return Response({"detail": "Utilisateur supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
    


#Mis à jour profile utilisateur
class UserUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # L'utilisateur ne peut mettre à jour que son propre compte
        return CustomUser.objects.filter(id=self.request.user.id)


#Liste utilisateur
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]  # ou IsAdminUser si réservé aux admins
    ilter_backends = [DjangoFilterBackend]
    filterset_fields = ['role']  # Filtre ?role=teacher|student|admin


#Modification de mot passe user
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        user = request.user

        if serializer.is_valid():
            # Vérifier l’ancien mot de passe
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            # Modifier le mot de passe
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)