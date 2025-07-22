from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
# from dj_rest_auth.app_settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer
from django.conf import settings
from django.utils.module_loading import import_string
from dj_rest_auth.serializers import UserDetailsSerializer

class UserDetailsSerializerMixin:
    def get_user_details_serializer_class(self):
        if hasattr(settings, 'REST_AUTH') and 'USER_DETAILS_SERIALIZER' in settings.REST_AUTH:
            return import_string(settings.REST_AUTH['USER_DETAILS_SERIALIZER'])
        return UserDetailsSerializer

class CustomRegisterView(UserDetailsSerializerMixin, RegisterView):

    # We are adding the missing helper method ourselves!
    def get_user_details_serializer_class(self):
        # Check if the setting is defined in REST_AUTH
        if hasattr(settings, 'REST_AUTH') and 'USER_DETAILS_SERIALIZER' in settings.REST_AUTH:
            # If yes, import and return it
            return import_string(settings.REST_AUTH['USER_DETAILS_SERIALIZER'])
        # If not, fall back to the library's default
        return UserDetailsSerializer

    # Your get_response_data method can now stay exactly as it was,
    # because the helper method it needs now exists.
    def get_response_data(self, user):
        refresh = RefreshToken.for_user(user)
        
        # Now this line will work!
        user_data_serializer_class = self.get_user_details_serializer_class()
        user_data = user_data_serializer_class(
            instance=user, 
            context=self.get_serializer_context()
        ).data

        response_data = {
            'user': user_data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
        
        return response_data
    

# user/views.py

class CustomLoginView(UserDetailsSerializerMixin, LoginView):
    # We'll override the method that generates the final response
    def get_response(self):
        # The original response (which is just a 200 OK)
        original_response = super().get_response()

        # The user object is attached to the view after successful login
        user = self.user

        # Get the tokens
        refresh = RefreshToken.for_user(user)

        # Use the same serializer logic from your Register view
        user_data_serializer_class = self.get_user_details_serializer_class()
        user_data = user_data_serializer_class(
            instance=user,
            context={'request': self.request}
        ).data

        # Add the user and token data to the response
        original_response.data.update({
            'user': user_data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })

        return original_response


class UserProfileView(APIView):
    """
    View to retrieve the current user's profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileSerializer(user, context={'request': request})
        return Response(serializer.data)