from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import ProfilePageImage
from .serializers import ImageSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsStartupOwner


class ImageView(GenericAPIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, IsStartupOwner)
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):
        file_serializer = self.get_serializer(
            data=request.data
        )

        if file_serializer.is_valid():
            data = file_serializer.save()
            response = {"success": "1", "file": {"url": data.image.url}}
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, *args, **kwargs):
        images = ProfilePageImage.objects.all().filter(startup_profile_id=kwargs["startup_profile_id"])
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)
