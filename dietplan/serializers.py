from rest_framework import serializers

class DietPlanSerializer(serializers.Serializer):
    user = serializers.JSONField(required=False, default=dict)