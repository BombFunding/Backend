from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer, ProjectImageSerializer, DashboardProjectSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from starboard.serializers import ProjectListSerializer as DashboardProjectSerializer

class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        return Project.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Get all projects"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a project (the user must be authenticated)"
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ProjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Project.objects.none()
        return Project.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this project.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this project.")
        instance.delete()

    @swagger_auto_schema(
        operation_description="Get a project",
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="ID of the project",
                required=True,
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a project (the user must be authenticated)",
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="ID of the project",
                required=True,
            )
        ]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Delete a project (the user must be authenticated)",
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="ID of the project",
                required=True,
            )
        ]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a project (the user must be authenticated)",
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="ID of the project",
                required=True,
            )
        ]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

class ProjectImageView(generics.CreateAPIView):
    serializer_class = ProjectImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            "success": 1,
            "file": {
                "url": response.data["image"],
            }
        }
        return Response(response.data, status=201)

    @swagger_auto_schema(
        operation_description="Upload an image for a project (the user must be authenticated)"
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class StartupProjectsList(generics.ListAPIView):
    serializer_class = DashboardProjectSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Project.objects.filter(user__username=self.kwargs["startup_username"])

    @swagger_auto_schema(
        operation_description="Get all projects of a startup",
        manual_parameters=[
            openapi.Parameter(
                name="startup_username",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                description="Username of the startup",
                required=True,
            )
        ]
    )
        
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ProjectDetailView(generics.RetrieveAPIView):
    serializer_class = DashboardProjectSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Project.objects.filter(id=self.kwargs["pk"])

    @swagger_auto_schema(
        operation_description="Get details of a single project by project_id",
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="ID of the project",
                required=True,
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)