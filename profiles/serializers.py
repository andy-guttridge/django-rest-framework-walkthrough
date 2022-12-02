from rest_framework import serializers
from .models import Profile
from followers.models import Follower


class ProfileSerializer(serializers.ModelSerializer):
    # Make the owner field read only, and overwrite the default
    # value (which would be the user id) with the username.
    owner = serializers.ReadOnlyField(source='owner.username')
    # Add an is_owner field which enables us to track whether the user
    # is the owner of the current profile. This is for our convenience
    # in the frontend when deciding which UI elements to render etc.
    # The SerializeMethodField method gets its value by calling a method
    # on our serializer class called get_fieldname.
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    # Here we add additional fields we've created in our views.py file to the
    # serializer
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()

    # Method to provide a value for our is_owner field.
    # Note we can access the request as it is passed in from the methods
    # in the views.py file.
    def get_is_owner(self, obj):
        request = self.context['request']
        # Check if the current user is the owner of the profile, and
        # return the result.
        return request.user == obj.owner
    
    # Populate the following_id field. If the user is authenticated,
    # check if this profile is one the user is following.
    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        # Return None if ther user isn't authenticated
        return None

    class Meta:
        model = Profile
        # Here we specify the fields we want to include in the serialized data.
        # Note the id field is created automatically on our model by Django,
        # but we still have to specify it if we want to include it in the
        # serialized data.
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner', 'following_id',
            'posts_count', 'followers_count', 'following_count'
        ]
