from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import *

User = get_user_model()
class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SenOtpSerializers


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "OTP ketdi! "})
        return Response(serializer.errors)



class VerifyView(APIView):
    permission_classes = [AllowAny]
    serializer_class = VerifySerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()

        refresh = RefreshToken.for_user(user=user)

        return Response({
            'message': 'Login buldi', 
            'refresh': str(refresh), 
            'access': str(refresh.access_token)
        }, status=200)