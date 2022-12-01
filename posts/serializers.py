from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    is_owner = serializers.SerializerMethodField()

    # The validator method's name is always validate_fieldname.
    # We use this to validate the image, to make sure the file size,
    # height and width are within appropriate limits. If not, we raise
    # validation errors with an appropriate message.
    def validate_image():
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

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'title', 'content',
            'image', 'profile_id', 'profile_image', 'is_owner', 'image_filter'
        ]
