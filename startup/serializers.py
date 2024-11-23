from rest_framework import serializers

from .models import StartupComment, StartupPosition, StartupProfile


class StartupProfileSerializer(serializers.ModelSerializer):
    startup_user_username = serializers.CharField(
        source="startup_user.username.username", read_only=True
    )
    email = serializers.EmailField(source="startup_user.email", read_only=True)
    socials = serializers.JSONField(required=False, allow_null=True)
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    header_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = StartupProfile
        fields = [
            "id",
            "startup_user_username",
            "email",
            "name",
            "bio",
            "page",
            "categories",
            "socials",
            "phone",
            "first_name",
            "last_name",
            "profile_picture",
            "header_picture",
        ]

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.bio = validated_data.get("bio", instance.bio)
        instance.page = validated_data.get("page", instance.page)
        instance.categories = validated_data.get("categories", instance.categories)
        instance.socials = validated_data.get("socials", instance.socials)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)

        if "profile_picture" in validated_data:
            instance.profile_picture = validated_data.get(
                "profile_picture", instance.profile_picture
            )
        if "header_picture" in validated_data:
            instance.header_picture = validated_data.get(
                "header_picture", instance.header_picture
            )

        instance.save()
        return instance


class StartupPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartupPosition
        fields = ["name", "bio", "total", "funded", "is_done", "start_time", "end_time"]


class StartupCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="username.username")

    startup_profile = serializers.CharField(source="startup_profile.name")

    class Meta:
        model = StartupComment
        fields = ["id", "startup_profile", "username", "comment", "time"]
