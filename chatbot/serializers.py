from rest_framework import serializers

class ChatbotSerializer(serializers.Serializer):
    question = serializers.CharField()
    additional_info = serializers.JSONField(required=False, default=dict)
