from rest_framework import serializers
from .models import Post
from likes.models import Like


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    is_owner = serializers.SerializerMethodField()
    like_id = serializers.SerializerMethodField()
    comments_count = serializers.ReadOnlyField()
    likes_count = serializers.ReadOnlyField()

    # The validator method's name is always validate_fieldname.
    # We use this to validate the image, to make sure the file size,
    # height and width are within appropriate limits. If not, we raise
    # validation errors with an appropriate message.
    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size larger than 2MB'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width greater than 4096px'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height greater than 4096px'
            )
        # We have to remember to return the original value which has been
        # passed in to this method if no error was raised.
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner
    
    # Populate the like_id field. If user is authenticated,
    # check is this post is one the user has liked.
    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, post=obj
            ).first()
            return like.id if liked else None
        # Return None if ther user isn't authenticated
        return None

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'title', 'content',
            'image', 'profile_id', 'profile_image', 'is_owner', 'image_filter',
            'like_id', 'comments_count', 'likes_count'
        ]
