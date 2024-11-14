from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import BasicUserProfile, BasicUser
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import BasicUserProfile

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "email": user.email,
             "name": user.name,
             "user_type": user.user_type,
             "access_token": access_token,
             "refresh_token": str(refresh)
             }
        , status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_own_basic_user_profile(request):
    user = request.user  
    try:
        
        basic_user_profile = BasicUserProfile.objects.get(username=user)

        
        profile_picture_url = None
        if basic_user_profile.profile_picture:
            profile_picture_url = request.build_absolute_uri(basic_user_profile.profile_picture.url)

        return Response({
            'basic_user_profile': {
                'username': user.username,
                'email': user.email,
                'about_me': user.about_me,
                'interests': basic_user_profile.interests,
                'password': user.password,
                'profile_picture': profile_picture_url  
            }
        }, status=status.HTTP_200_OK)
    
    except BasicUserProfile.DoesNotExist:
        return Response({'detail': 'Basic user profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def view_basic_user_profile(request, username):
    try:
        
        basic_user_profile = BasicUserProfile.objects.get(username__username=username)
        user = basic_user_profile.username

        
        profile_picture_url = None
        if basic_user_profile.profile_picture:
            profile_picture_url = request.build_absolute_uri(basic_user_profile.profile_picture.url)

        return Response({
            'basic_user_profile': {
                'username': user.username,
                'email': user.email,
                'about_me': user.about_me,
                'profile_picture': profile_picture_url  
            }
        }, status=status.HTTP_200_OK)

    except BasicUserProfile.DoesNotExist:
        return Response({'detail': 'Basic user profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
