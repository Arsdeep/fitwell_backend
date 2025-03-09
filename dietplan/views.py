import base64
from openai import OpenAI
from django.conf import settings
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
            additional_info = serializer.validated_data['additional_info']
            
            prompt = "Your job is to make a balanced diet while keeping in mind user details given below. Provide a structured JSON response containing the ingredient and dish names, the amount of calories+protien+carbs+fat it has. Format the response as follows:\n\n"
            
            structure = """
            {
    "breakfast": {
      "time": "08:00 AM",
      "item": {
        "name": "Oatmeal",
        "qty": "1 bowl",
        "cal": 250,
        "carbs": "45g",
        "protein": "8g",
        "fat": "5g"
      }
    },
    "lunch": {
      "time": "01:00 PM",
      "item": {
        "name": "Grilled Chicken",
        "qty": "150g",
        "cal": 250,
        "carbs": "0g",
        "protein": "40g",
        "fat": "6g"
      }
    },
    "snack": {
      "time": "04:30 PM",
      "item": {
        "name": "Greek Yogurt",
        "qty": "1 cup",
        "cal": 150,
        "carbs": "10g",
        "protein": "20g",
        "fat": "2g"
      }
    },
    "dinner": {
      "time": "07:30 PM",
      "item": {
        "name": "Salmon",
        "qty": "120g",
        "cal": 250,
        "carbs": "0g",
        "protein": "25g",
        "fat": "15g"
      }
    }
  }
}"""
            
            prompt += structure
            
            message = [{"role": "system", "content": prompt}]
                
            message += [{"role": "user", "content": f"Give a diet plan based on these user details - {additional_info}"}]
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=message,
                response_format={"type": "json_object"},
            )

            # Extract response
            answer = response.choices[0].message.content
            try:
                answer = loads(answer)
                return Response({"diet_plan": answer}, status=status.HTTP_200_OK)
            except JSONDecodeError:
                return {"error": "Roadmap content is not a valid JSON."}

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
