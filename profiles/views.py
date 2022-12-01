from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsOwnerOrReadOnly


class ProfileList(APIView):
    """
    The profiles list view which returns all the profiles as JSON
    """
    def get(self, request):
        profiles = Profile.objects.all()
        # Create a serializer instance. many=True specifies that we are
        # serializing multiple profile instances. Note we pass the request
        # to our serializer object so that it has access.
        serializer = ProfileSerializer(
            profiles, many=True, context={'request': request}
            )
        # Instead of returning objects like we might in a template based Django
        # app, we return the data from our serializer.
        return Response(serializer.data)


class ProfileDetail(APIView):
    """
    The detail view GET request returns one profile by the
    primary key which is specified in the URL.
    """
    # This line gets Django to automatically create a form in
    # the browser to enable us to edit our profile data.
    serializer_class = ProfileSerializer
    # Here we specify our permission classes. This is a property
    # of APIView.
    permission_classes = [IsOwnerOrReadOnly]
    # get_object method is a self defined method, not a standard
    # Django one. We use this to look for the profile and either
    # retrieve it or return a 404 error
    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            # Check if user has permission for the request they have made.
            # If not, the 403 forbidden error is returned instead of the profile.
            self.check_object_permissions(self.request, profile)
            return profile
        except Profile.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        profile = self.get_object(pk)
        # This time we are only dealing with a single profile instance, 
        # not a queryset, so no need for many=True.
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        # Call get_object to attempt to retrieve the profile
        profile = self.get_object(pk)
        # Create a serializer instance using the retrieved profile and
        # request data
        serializer = ProfileSerializer(
            profile, data=request.data, context={'request': request}
            )
        # Validate and save the serialized data to the database if it is,
        # and return the data as the response.
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # Or if not valid, return the error data with HTTP 400 error status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)