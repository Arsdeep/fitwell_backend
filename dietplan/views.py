import base64
from openai import OpenAI
from django.conf import settings
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DietPlanSerializer
from json import JSONDecodeError, loads

client = OpenAI(api_key=settings.OPENAI_API_KEY)  # Initialize OpenAI client

class DietPlanAPIView(APIView):
    def post(self, request):
        serializer = DietPlanSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Check if cached response exists
            cached_plan = cache.get(f'diet_plan_{user["uid"]}')
            if cached_plan:
                return Response({"diet_plan": cached_plan}, status=status.HTTP_200_OK)

            # Generate diet plan if not in cache
            prompt = """Your job is to make a balanced diet while keeping in mind user details given below. Add local dishes catered to the user's nationality. Provide a structured JSON response containing the ingredient and dish names, the amount of calories, protein, carbs, and fat. Format the response as follows:\n\n"""
            
            structure = """{
  "breakfast": {
    "time": "08:00 AM",
    "item": {
      "name": "<Breakfast Item>",
      "qty": "<Quantity>",
      "cal": 250,
      "carbs": "45g",
      "protein": "8g",
      "fat": "5g"
    }
  },
  "lunch": {
    "time": "01:00 PM",
    "item": {
      "name": "<Lunch Item>",
      "qty": "<Quantity>",
      "cal": 250,
      "carbs": "0g",
      "protein": "40g",
      "fat": "6g"
    }
  },
  "snack": {
    "time": "04:30 PM",
    "item": {
      "name": "<Snack Item>",
      "qty": "<Quantity>",
      "cal": 150,
      "carbs": "10g",
      "protein": "20g",
      "fat": "2g"
    }
  },
  "dinner": {
    "time": "07:30 PM",
    "item": {
      "name": "<Dinner Item>",
      "qty": "<Quantity>",
      "cal": 250,
      "carbs": "0g",
      "protein": "25g",
      "fat": "15g"
    }
  }
}
"""
            prompt += structure

            message = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Give a diet plan based on these user details - {user}"}
            ]

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=message,
                response_format={"type": "json_object"},
            )

            try:
                answer = loads(response.choices[0].message.content)
                # Cache the response for future requests
                cache.set(f'diet_plan_{user["uid"]}', answer, timeout=86400)  # Cache for 1 day
                return Response({"diet_plan": answer}, status=status.HTTP_200_OK)
            except JSONDecodeError:
                return Response({"error": "Generated diet plan is not a valid JSON."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)