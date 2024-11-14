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
        header_picture_url = None
        if basic_user_profile.profile_picture:
            profile_picture_url = request.build_absolute_uri(basic_user_profile.profile_picture.url)
        if basic_user_profile.header_picture:
            header_picture_url = request.build_absolute_uri(basic_user_profile.header_picture.url)

        return Response({
            'basic_user_profile': {
                'username': user.username,
                'email': user.email,
                'about_me': user.about_me,
                'interests': basic_user_profile.interests,
                'password': user.password,
                'profile_picture': profile_picture_url,  
                'header_picture': header_picture_url  
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
        header_picture_url = None
        if basic_user_profile.profile_picture:
            profile_picture_url = request.build_absolute_uri(basic_user_profile.profile_picture.url)
        if basic_user_profile.header_picture:
            header_picture_url = request.build_absolute_uri(basic_user_profile.header_picture.url)

        return Response({
            'basic_user_profile': {
                'username': user.username,
                'email': user.email,
                'about_me': user.about_me,
                'profile_picture': profile_picture_url,
                'header_picture': header_picture_url  
            }
        }, status=status.HTTP_200_OK)

    except BasicUserProfile.DoesNotExist:
        return Response({'detail': 'Basic user profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_basic_user_profile(request):
    user = request.user  
    try:
        basic_user_profile, created = BasicUserProfile.objects.get_or_create(username=user)

        data = request.data
        
        if 'about_me' in data:
            user.about_me = data['about_me']  
        if 'email' in data:
            user.email = data['email']  
        if 'password' in data:
            user.set_password(data['password'])  
        
        user.save()  
        if 'interests' in data:
            basic_user_profile.interests = data['interests']
        if 'profile_picture' in request.FILES:
            basic_user_profile.profile_picture = request.FILES['profile_picture']
        if 'header_picture' in request.FILES:
            basic_user_profile.header_picture = request.FILES['header_picture']
        
        basic_user_profile.save()  

        return Response({'detail': 'Profile updated successfully.'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
