from openai import OpenAI
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChatbotSerializer

client = OpenAI(api_key=settings.OPENAI_API_KEY)  # Initialize OpenAI client

class ChatbotAPIView(APIView):
    def post(self, request):
        serializer = ChatbotSerializer(data=request.data)
        if serializer.is_valid():
            
            prompt = f"""
            You are FitWell AI assistant, a knowledgeable wellness and fitness chatbot. Provide helpful and accurate answers to user queries about health, fitness, and well-being. 
            Consider the user's background information if provided in additional details when answering. 
            """
            
            question = serializer.validated_data['question']
            additional_info = serializer.validated_data.get('additional_info', {})
            
            message = [{"role": "system", "content": prompt}]
            
            if additional_info != {}:
                message += [{"role": "system", "content": f"Additional Details of User : {additional_info}"}]
                
            message += [{"role": "user", "content": question}]
            
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=message,
            )

            answer = completion.choices[0].message.content
            return Response({"answer": answer}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
