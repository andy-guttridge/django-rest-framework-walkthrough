from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from likes.models import Like
from likes.serializers import LikeSerializer


# We subclass ListCreateAPIView so that we get our
# GET and POST methods for free.
class LikeList(generics.ListCreateAPIView):
    # Ensure only authenticated users can create a like
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    # Use the perform_create method to set the owner of the like
    # to the user making the request.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# We sub-class the RetrieveDestroyAPI view, as we only want to retrieve
# and delete likes. There's no need to update.
class LikeDetail(generics.RetrieveDestroyAPIView):
    # Ensure only authenticated users can create a like
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()