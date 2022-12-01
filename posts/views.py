from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer


class PostList(APIView):
    # Causes Django to render a form for the Posts class
    serializer_class = PostSerializer
    
    # Remember permission_classes is a method of the superclass.
    # Here we use the IsAuthenticatedOrReadOnly permission provided by Django.
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get(self, request):
        # Retrieve all posts, serialize them and return the JSON data
        posts = Post.objects.all()
        serializer = PostSerializer(
            posts, many=True, context={'request': request}
            )
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(
            data=request.data, context={'request': request}
        )
        # Use the serializer to validate the posted data. Save the post
        # and return HTTP success code if successful, otherwise return
        # the error details from the serializer and 400 error.
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
