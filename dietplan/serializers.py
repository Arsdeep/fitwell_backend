from rest_framework import serializers

class DietPlanSerializer(serializers.Serializer):
    additional_info = serializers.JSONField(required=False, default=dict)