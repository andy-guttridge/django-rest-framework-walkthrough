from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer


# We want to both create and list comments in the list view.
# Instead of explicitly defining POST and GET methods like we did
# for posts, we extend the generics.ListCreateAPIView class.
# This means that we don't have to write the GET or POST methods.
# ListAPI view comes with a GET method, CreateAPI view comes with a
# POST method. The HTTP request is part of the context object by default when
# using generics, so we don't have to pass these to the serializer manually
# like we did in our GET and POST requests.
class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    # Prevent anonymous users from commenting
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # We set the queryset attribute, rather than just specifying the model
    # we want to use - this is the way DRF works.
    # This means it is possible to filter out some of the
    # model instances if need be. We could use this to ensure users can only
    # access their own data, e.g. sensitive data like payments, account
    # details etc.
    queryset = Comment.objects.all()
    filter_backends = [
        # Add DjangoFilterBackend
        DjangoFilterBackend,
    ]

    # Fields for DjangoFilterBackend
    filterset_fields = [
        'post'
    ]

    # We use the Django define perform_create method to ensure comments
    # are associated with a user upon creation.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# Here we sub-class RetrieveUpdateDestroyAPI view which gives us GET, PUT and
# DELETE functionality.
class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    # Ensure only the comment owner can edit the post
    permission_classes = [IsOwnerOrReadOnly]
    # We use the CommentDetailSerializer so as not to have to send the post id
    # with every request
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()