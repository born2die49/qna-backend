from dj_rest_auth.registration.views import RegisterView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from dj_rest_auth.app_settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer

class CustomRegisterView(RegisterView):
  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = self.perform_create(serializer)
    headers = self.get_success_headers(serializer.data)

    # Use the configured UserDetailsSerializer to get user data
    user_data_serializer = api_settings.USER_DETAILS_SERIALIZER
    user_data = user_data_serializer(user, context={'request': request}).data

    # Generate tokens for the user
    refresh = RefreshToken.for_user(user)
    
    # The response now includes user data and tokens
    response_data = {
        'user': user_data,
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }

    return Response(
        response_data,
        status=status.HTTP_201_CREATED,
        headers=headers
    )


class UserProfileView(APIView):
    """
    View to retrieve the current user's profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileSerializer(user, context={'request': request})
        return Response(serializer.data)