from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from authenticator.models import BaseUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import LikedSubcategories
from .serializers import LikedSubcategoriesSerializer, CategoryOperationSerializer

class UserLikedCategoriesView(generics.GenericAPIView):
    serializer_class = LikedSubcategoriesSerializer
    permission_classes = [IsAuthenticated]
    category_param = openapi.Parameter(
        'username', 
        openapi.IN_PATH,
        description='Username of the base user or investor',
        type=openapi.TYPE_STRING
    )

    def get_user(self, username):
        user = get_object_or_404(BaseUser, username=username)
        if hasattr(user, 'startup'):
            return Response(
                {"error": "Startups cannot have liked subcategories"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return user

    def check_user_permission(self, request_user, target_username):
        if request_user.username != target_username:
            return Response(
                {"error": "You can only modify your own subcategories"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return None

    @swagger_auto_schema(
        operation_description="Get user's liked subcategories",
        manual_parameters=[category_param],
        responses={200: LikedSubcategoriesSerializer}
    )
    def get(self, request, username):
        user = self.get_user(username)
        if isinstance(user, Response):
            return user
        
        liked_categories, _ = LikedSubcategories.objects.get_or_create(user=user)
        serializer = self.serializer_class(liked_categories)
        return Response({"subcategories": serializer.data['subcategories']}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Add a subcategory to user's liked categories",
        manual_parameters=[category_param],
        request_body=CategoryOperationSerializer,
        responses={
            201: 'Subcategory added successfully',
            400: 'Subcategory already exists',
            403: 'Permission denied'
        }
    )
    def post(self, request, username):
        permission_check = self.check_user_permission(request.user, username)
        if permission_check:
            return permission_check

        user = self.get_user(username)
        if isinstance(user, Response):
            return user

        serializer = CategoryOperationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        liked_categories, _ = LikedSubcategories.objects.get_or_create(user=user)
        subcategory = serializer.validated_data['subcategory']
        
        if subcategory in liked_categories.subcategories:
            return Response(
                {
                    "error": f"Subcategory '{subcategory}' is already in your liked subcategories",
                    "current_subcategories": liked_categories.subcategories
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )

        liked_categories.add_subcategory(subcategory)
        
        return Response(
            {
                "message": f"Subcategory '{subcategory}' added successfully",
                "current_subcategories": liked_categories.subcategories
            }, 
            status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(
        operation_description="Remove a subcategory from user's liked categories",
        manual_parameters=[category_param],
        request_body=CategoryOperationSerializer,
        responses={
            200: 'Subcategory removed successfully',
            400: 'Subcategory does not exist in liked subcategories',
            403: 'Permission denied'
        }
    )
    def delete(self, request, username):
        permission_check = self.check_user_permission(request.user, username)
        if permission_check:
            return permission_check

        user = self.get_user(username)
        if isinstance(user, Response):
            return user

        serializer = CategoryOperationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        liked_categories, _ = LikedSubcategories.objects.get_or_create(user=user)
        subcategory = serializer.validated_data['subcategory']

        if subcategory not in liked_categories.subcategories:
            return Response(
                {
                    "error": f"Subcategory '{subcategory}' is not in your liked subcategories",
                    "current_subcategories": liked_categories.subcategories
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )

        liked_categories.remove_subcategory(subcategory)
        
        return Response(
            {
                "message": f"Subcategory '{subcategory}' removed successfully",
                "current_subcategories": liked_categories.subcategories
            }, 
            status=status.HTTP_200_OK
        )
