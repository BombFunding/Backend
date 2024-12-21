from rest_framework import status, mixins, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import InvestorProfile
from authenticator.models import InvestorUser
from .serializers import InvestorProfileSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import GenericAPIView
from .models import InvestorProfile , InvestorUser
from .models import InvestorVote
from .serializers import VoteSerializer
from .serializers import InvestorProfileSerializer
from django.db import IntegrityError


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

        if request.user.is_authenticated and request.user.username != username:
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


class VoteProfile(GenericAPIView):
    permission_classes = [AllowAny]

    def get_permissions(self):
        """
        Different permission classes for functions
        """
        if self.request.method in ["POST", "DELETE"]:
            return [IsAuthenticated()]
        return super().get_permissions()

    @swagger_auto_schema(
        request_body=VoteSerializer,
        responses={
            201: "Vote added successfully.",
            200: "Vote updated successfully.",
            400: "Invalid vote type.",
            404: "investor profile not found.",
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Vote on an investor profile (like or nothing).
        """
        user = request.user  
        investor_profile_id = self.kwargs.get("investor_profile_id")
        vote_type = request.data.get("vote")

        if vote_type not in [1, 0]:  
            return Response(
                {"detail": "Invalid vote type."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            investor_profile = InvestorProfile.objects.get(pk=investor_profile_id)
        except InvestorProfile.DoesNotExist:
            return Response(
                {"detail": "Investor profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            # Checking if an existing vote exists
            existing_vote = InvestorVote.objects.filter(
                user=user, investor_profile=investor_profile
            ).first()

            if vote_type == 1:  
                if existing_vote and existing_vote.vote == 1:
                    return Response(
                        {"detail": "You have already liked this profile."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                
                # Create or update the vote to 1
                InvestorVote.objects.update_or_create(
                    user=user, investor_profile=investor_profile, defaults={"vote": 1}
                )
                
                # Handle profile stats (ensure using correct field)
                profile_statics, _ = InvestorProfile.objects.get_or_create(
                    investor_user=investor_profile.investor_user
                )
                profile_statics.add_like(liked_by_user=user.username)
                
                return Response(
                    {"detail": "Profile liked successfully."},
                    status=status.HTTP_201_CREATED,
                )

            elif vote_type == 0:  
                if existing_vote and existing_vote.vote == 1:
                    # Removing like if it exists
                    profile_statics = InvestorProfile.objects.filter(
                        investor_user=investor_profile.investor_user
                    ).first()
                    
                    if profile_statics:
                        profile_statics.remove_like(liked_by_user=user.username)
                    existing_vote.delete()
                    
                    return Response(
                        {"detail": "Like removed successfully."},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"detail": "No like exists to remove."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

        except IntegrityError:
            return Response(
                {"detail": "An error occurred while processing your vote."},
                status=status.HTTP_400_BAD_REQUEST,
            )


    @swagger_auto_schema(
        responses={
            200: "Vote count retrieved successfully.",
            404: "investor profile not found.",
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Get the vote count of a investor profile.
        """
        investor_profile_id = self.kwargs.get("investor_profile_id")

        try:
            investor_profile = InvestorProfile.objects.get(pk=investor_profile_id)
        except InvestorProfile.DoesNotExist:
            return Response(
                {"detail": "investor profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        vote_count = investor_profile.score
        return Response(
            {"vote_count": vote_count},
            status=status.HTTP_200_OK,
        )