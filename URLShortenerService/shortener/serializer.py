from rest_framework import serializers
from .models import URL

class db_serializer(serializers.ModelSerializer):
    class Meta:
        model=URL
        fields=('uid','long_url', 'short_url')

class short_url_response_serializer(serializers.Serializer):
    short_url = serializers.CharField(max_length = 100)
