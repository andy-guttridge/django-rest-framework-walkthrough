from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


# Add the profile_id and profile_image fields to the
# details of the currently authenticated
# user returned to the client.
class CurrentUserSerializer(UserDetailsSerializer):
    profile_id = serializers.ReadOnlyField(source='profile.id')
    profile_image = serializers.ReadOnlyField(source='profile.image.url')

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            'profile_id', 'profile_image'
        )
