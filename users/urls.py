from django.urls import path

from .views import RegistrationAPIView, MyTokenObtainPairView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('register', RegistrationAPIView.as_view()),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]