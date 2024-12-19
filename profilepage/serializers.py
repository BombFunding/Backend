from rest_framework import serializers
from .models import ProfilePageImage
from startup.models import StartupProfile
from authenticator.models import StartupUser
from authenticator.utils import get_instance

def get_profile(user, startup_profile_id):
    print(user, startup_profile_id)
    startup_user = get_instance(StartupUser, username=user)
    if not startup_user:
        return None
    startup_profile = get_instance(StartupProfile, id=startup_profile_id, startup_user=startup_user)
    return startup_profile

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfilePageImage
        fields = ["image"]

    def save(self, **kwargs):
        user = self.context['request'].user
        startup_profile_id = self.context["view"].kwargs.get("startup_profile_id")
        profile = get_profile(user, startup_profile_id)
        image = self.validated_data['image']
        pimage = ProfilePageImage.objects.create(startup_profile=profile, image=image)
        pimage.save()

        return pimage