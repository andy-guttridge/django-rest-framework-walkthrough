from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        # Create a serializer instance. many=True specifies that we are
        # serializing multiple profile instances.
        serializer = ProfileSerializer(profiles, many=True)
        # Instead of returning objects like we might in a template based Django
        # app, we return the data from our serializer.
        return Response(serializer.data)
