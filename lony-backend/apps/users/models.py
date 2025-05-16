# lony_backend/users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'student', 'Étudiant'
        TEACHER = 'teacher', 'Enseignant'
        ADMIN   = 'admin',   'Administrateur'

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    # 🔸 Méthodes personnalisées
    def is_student(self):
        return self.role == self.Role.STUDENT

    def is_teacher(self):
        return self.role == self.Role.TEACHER
    
    def is_admin(self):
        return self.role == self.Role.ADMIN



def avatar_upload_path(instance, filename):
    return f"avatars/user_{instance.user.id}/{filename}"

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Profil de {self.user.username}"