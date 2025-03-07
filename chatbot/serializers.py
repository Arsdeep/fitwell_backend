from rest_framework import serializers

class ChatbotSerializer(serializers.Serializer):
    question = serializers.CharField()
