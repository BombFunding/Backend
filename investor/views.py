from rest_framework import status, mixins, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import InvestorProfile
from authenticator.models import InvestorUser
from .serializers import InvestorProfileSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class InvestorProfileRetrieveView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = InvestorProfile.objects.all()
    serializer_class = InvestorProfileSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Get the profile of an Investor user",
        responses={
            200: openapi.Response(
                description="Profile retrieved successfully.",
            ),
            404: openapi.Response(
                description="Not Found",
                examples={"application/json": {"detail": "Profile not found."}},
            ),
        },
    )
    def get(self, request, username):
        try:
            investor_user = InvestorUser.objects.get(username__username=username)
        except InvestorUser.DoesNotExist:
            return Response({"detail": "Investor user not found."}, status=status.HTTP_404_NOT_FOUND)

        investor_profile = InvestorProfile.objects.filter(investor_user=investor_user).first()

        if not investor_profile:
            return Response({"detail": "Investor profile not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user.username != username:
            investor_profile.investor_profile_visit_count += 1
            investor_profile.save()
            from profile_statics.models import ProfileStatics

            profile_statics, _ = ProfileStatics.objects.get_or_create(user=investor_user.username)
            profile_statics.increment_view()

        serializer = self.get_serializer(investor_profile)
        return Response({"profile": serializer.data}, status=status.HTTP_200_OK)


class InvestorProfileUpdateView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = InvestorProfile.objects.all()
    serializer_class = InvestorProfileSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update an Investor Profile",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "bio": openapi.Schema(type=openapi.TYPE_STRING, description="Biography of the investor"),
                "experience": openapi.Schema(type=openapi.TYPE_STRING, description="Experience details of the investor"),
                "linkedin_profile": openapi.Schema(type=openapi.TYPE_STRING, description="LinkedIn profile URL"),
                
            },
            required=["bio"],  
        ),
        responses={
            200: openapi.Response(
                description="Investor profile updated successfully.",
            ),
            400: openapi.Response(
                description="Validation error",
            ),
        },
    )
    def patch(self, request):
        user = request.user
        try:
            investor_user = InvestorUser.objects.get(username=user)
        except InvestorUser.DoesNotExist:
            return Response({"detail": "Investor user not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            investor_profile = InvestorProfile.objects.get(investor_user=investor_user)
        except InvestorProfile.DoesNotExist:
            return Response({"detail": "Investor profile not found."}, status=status.HTTP_404_NOT_FOUND)

        
        excluded_fields = ["investor_profile_visit_count", "score"]
        update_data = {key: value for key, value in request.data.items() if key not in excluded_fields}

        
        serializer = self.get_serializer(investor_profile, data=update_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Investor profile updated successfully.", "profile": serializer.data},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
