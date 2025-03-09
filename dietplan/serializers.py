from rest_framework import serializers

class DietPlanSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    additional_info = serializers.JSONField(required=False, default=dict)