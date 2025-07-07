from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile data retrieval and updates.
    Used for the /profile/ endpoint.
    """
    # This new field will call the get_avatar_url method
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        # Add 'avatar_url' to the list of fields
        fields = ['id', 'email', 'name', 'avatar', 'avatar_url']
        read_only_fields = ['id', 'email']

    # This method gets the value for the 'avatar_url' field
    def get_avatar_url(self, obj):
        return obj.avatar_url()
