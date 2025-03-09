from rest_framework import serializers

class ChatbotSerializer(serializers.Serializer):
    prev_question = serializers.CharField(required=False, default=dict)
    prev_answer = serializers.CharField(required=False, default=dict)
    question = serializers.CharField(required=True)
    additional_info = serializers.JSONField(required=False, default=dict)
