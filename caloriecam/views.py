import base64
from openai import OpenAI
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageUploadSerializer, FoodSearchSerializer
from json import JSONDecodeError, loads

client = OpenAI(api_key=settings.OPENAI_API_KEY)  # Initialize OpenAI client

class FoodCalorieAPIView(APIView):
    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image = request.FILES['image']  # Correctly get the uploaded image file
            
            # Encode the image in Base64
            base64_image = base64.b64encode(image.read()).decode("utf-8")
            
            prompt = "Your job is to Analyze the given image and identify all food items present. Provide a structured JSON response containing the number of detected food items, their names, and an estimated calorie+protien+carbs+fat count for each. Also add serving size detail in count. Format the response as follows:\n\n"
            
            structure = """{
                "foods": [
                    {
                    "name": "<food_name>",
                    "count": "<estimated_count>"
                    "calories": "<estimated_calories>",
                    "protien": "<estimated_protien>",
                    "carbs": "<estimated_carbs>",
                    "fat": "<estimated_fat>"
                    },
                    {
                    "name": "<food_name>",
                    "count": "<estimated_count>"
                    "calories": "<estimated_calories>",
                    "protien": "<estimated_protien>",
                    "carbs": "<estimated_carbs>",
                    "fat": "<estimated_fat>"
                    }
                ]
                }
                """
            
            prompt += structure

            # Send request to OpenAI Vision API
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user","content": [{"type": "text", "text": prompt},{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}],
                    }
                ],
                response_format={"type": "json_object"},
            )

            # Extract response
            answer = response.choices[0].message.content
            try:
                answer = loads(answer)
                return Response({"calories_info": answer}, status=status.HTTP_200_OK)
            except JSONDecodeError:
                return {"error": "Roadmap content is not a valid JSON."}

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FoodSearchAPIView(APIView):
    def post(self, request):
        serializer = FoodSearchSerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data['query']
            
            prompt = "Your job is to provide a list of 3 dishes related to the food item or dish itself based on the given food item/dish name. Provide a structured JSON response containing the dish name, the amount of calories+protien+carbs+fat it has. Format the response as follows:\n\n"
            
            structure = """{
                "foods": [
                    {
                    "name": "<food_name>",
                    "count": "<estimated_count>"
                    "calories": "<estimated_calories>",
                    "protien": "<estimated_protien>",
                    "carbs": "<estimated_carbs>",
                    "fat": "<estimated_fat>"
                    },
                    {
                    "name": "<food_name>",]
                    "count": "<estimated_count>"
                    "calories": "<estimated_calories>",
                    "protien": "<estimated_protien>",
                    "carbs": "<estimated_carbs>",
                    "fat": "<estimated_fat>"
                    }
                ]
                }
                """
            
            prompt += structure
            
            message = [{"role": "system", "content": prompt}]
                
            message += [{"role": "user", "content": f"Query of Food item/dish is - {query}"}]
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=message,
                response_format={"type": "json_object"},
            )

            # Extract response
            answer = response.choices[0].message.content
            try:
                answer = loads(answer)
                return Response({"calories_info": answer}, status=status.HTTP_200_OK)
            except JSONDecodeError:
                return {"error": "Roadmap content is not a valid JSON."}

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
