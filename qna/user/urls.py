from django.urls import path

from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.views import LoginView, LogoutView

from .views import UserProfileView, CustomRegisterView


urlpatterns = [
  path('register/', CustomRegisterView.as_view(), name='rest_register'),
  path('login/', LoginView.as_view(), name='rest_login'),
  path('logout/', LogoutView.as_view(), name='rest_logout'),
  path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
  path('profile/', UserProfileView.as_view(), name='user_profile'),
]