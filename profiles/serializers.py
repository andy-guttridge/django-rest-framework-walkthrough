from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    # Make the owner field read only, and overwrite the default
    # value (which would be the user id) with the username.
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Profile
        # Here we specify the fields we want to include in the serialized data.
        # Note the id field is created automatically on our model by Django,
        # but we still have to specify it if we want to include it in the
        # serialized data.
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image'
        ]
