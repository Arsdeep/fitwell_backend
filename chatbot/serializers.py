from rest_framework import serializers

class ChatbotSerializer(serializers.Serializer):
    prev_question = serializers.CharField(required=False)
    prev_answer = serializers.CharField(required=False)
    question = serializers.CharField()
    additional_info = serializers.JSONField(required=False, default=dict)
