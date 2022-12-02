from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions, filters
from django.db.models import Count
from django.http import Http404
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsOwnerOrReadOnly


class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """
    serializer_class = ProfileSerializer
    # Use annotate and Count to create a new field containing a count of the
    # number of posts retrieved.
    queryset = Profile.objects.annotate(
        # 'owner__post' performs a look-up from the Post model, through the
        # User model (owner is a foreign key to a user) to the Post model. We
        # have to do this because there is no direct link between the Profile
        # and Post model. distinct=True ensures only unique posts are counted,
        # because we are using annotate to create more than one field.
        # Otherwise, we would get duplicates.
        posts_count=Count('owner__post', distinct=True),
        # On the followers_count and following_count fields, we use the related
        # name defined in the Follower model for the look-ups, because the
        # Follower model has two foreign keys both pointing to user objects.
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    # Enable sorting by our backend and specify which fields we want to be able
    # to sort on. Note we have included two fields from the Follwers models, where
    # we use the underscores to perform a lookup.
    filter_backends = [
        filters.OrderingFilter
    ]
    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at'
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')