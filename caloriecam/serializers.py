from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()

class FoodSearchSerializer(serializers.Serializer):
    query = serializers.CharField()