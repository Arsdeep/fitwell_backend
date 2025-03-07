import base64
from openai import OpenAI
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageUploadSerializer

client = OpenAI(api_key=settings.OPENAI_API_KEY)  # Initialize OpenAI client

class FoodCalorieAPIView(APIView):
    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image = request.FILES['image']  # Correctly get the uploaded image file
            
            # Encode the image in Base64
            base64_image = base64.b64encode(image.read()).decode("utf-8")

            # Send request to OpenAI Vision API
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Identify the food items in this image and estimate their calorie content."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                        ],
                    }
                ],
            )

            # Extract response
            answer = response.choices[0].message.content
            return Response({"calories_info": answer}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
