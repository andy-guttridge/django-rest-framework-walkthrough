from django.db import IntegrityError
from rest_framework import serializers
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model
    The create method handles the unique constraint on 'owner' and 'post'
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = [
            'id', 'owner', 'post', 'created_at'
        ]

    # Create is a Django method of the super-class.
    # Here, we used it to catch if we are trying to create
    # a duplicate of an object that already exists and throw
    # an error if we are. Note that the model itself was defined
    # such that the owner and post to which the like is associated
    # have to be unique, so that then gives us an error if there is
    # an attempt to create a duplicate, which we can catch here.
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'Possible duplicate like'
            })

