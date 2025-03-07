from rest_framework import serializers

class ChatbotSerializer(serializers.Serializer):
    question = serializers.CharField()
    additionalinfo = serializers.JSONField(required=False, default=dict)
