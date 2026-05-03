from rest_framework import serializers
from .models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'image', 'watermarked', 'original_name', 'created_at']
        read_only_fields = ['watermarked']
