from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('liste/', UserListView.as_view(), name='user-list'),
    path('delete-user/<int:pk>/', UserByAdminDeleteView.as_view(), name='admin-user-delete'),
    path('<int:id>/', UserDetailView.as_view(), name='user-detail'),

    path('register/', UserCreateView.as_view(), name='user-register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('profile/', UserProfileDetail.as_view(), name='user-profile'), # à retirer après verification
    path('me/', UserMeView.as_view(), name='user-me'), 
    
    path('<int:id>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('<int:id>/update/', UserUpdateView.as_view(), name='user-update'),
    path('/change-password/', ChangePasswordView.as_view(), name='change-password'),

    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='token_verify'),  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)