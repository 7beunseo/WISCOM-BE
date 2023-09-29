from django.conf import settings
from rest_framework import serializers
from .models import Developer

class DeveloperSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Developer
        fields = ['post_number', 'name', 'image']

    def get_image(self, instance):
        if instance.image:
            image_url = str(instance.image).replace(settings.MEDIA_URL, '')
            return image_url
        else:
            return None