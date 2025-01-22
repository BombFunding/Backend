from rest_framework import serializers
from .models import Pin

class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pin
        fields = ['latitude', 'longitude']  # نیازی به افزودن فیلد user در اینجا نیست
