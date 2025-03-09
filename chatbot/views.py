from openai import OpenAI
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChatbotSerializer
import re

client = OpenAI(api_key=settings.OPENAI_API_KEY)  # Initialize OpenAI client

def process_string(s):
    matches = re.findall(r"<actionTrue=(\d+)>", s)
    total_calories = sum(map(int, matches))
    cleaned_string = re.sub(r"<actionTrue=\d+>", "", s)
    return total_calories, cleaned_string.strip()

class ChatbotAPIView(APIView):
    def post(self, request):
        serializer = ChatbotSerializer(data=request.data)
        if serializer.is_valid():
            
            prompt = f"""
            You are FitWell AI assistant, a knowledgeable wellness and fitness chatbot. Provide helpful and accurate answers to user queries about health, fitness, and well-being in short and concise manner.
            Give advice leaning towards fixing the user's diet if the user asks any queries about diseases or issues in their lives.
            Consider the user's background information if provided in additional details when answering.
            If user mentions any calorie burning activity, answer that the calories had been substracted, after that calculate the total calories burnt and add it at the end of the answer like - <actionTrue=calories_burnt>, dont add anything else.
            """
            
            question = serializer.validated_data['question']
            additional_info = serializer.validated_data.get('additional_info', {})
            
            message = [{"role": "system", "content": prompt}]
            
            if serializer.validated_data['prev_question']:
                message = [{"role": "user", "content": serializer.validated_data['prev_question']}]
                
            if serializer.validated_data['prev_answer']:
                message = [{"role": "system", "content": serializer.validated_data['prev_answer']}]
                
            if additional_info != {}:
                message += [{"role": "system", "content": f"Additional Details of User : {additional_info}"}]
                
            message += [{"role": "user", "content": question}]
            
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=message,
            )
            
            answer = completion.choices[0].message.content
            
            calories, answer = process_string(answer)

            return Response({"answer": answer, "calories_burnt": calories}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
