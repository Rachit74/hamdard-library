from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserLoginSerializer, UserRegisterSerializer


# helper function to generate tokens for a user
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


# POST user login view
@api_view(['POST'])
def login_user(request):
    serializer = UserLoginSerializer(data=request.data)

    if serializer.is_valid():
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'message': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        tokens = get_tokens_for_user(user=user)
        return Response(tokens, status=status.HTTP_200_OK)

        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)

    if serializer.is_valid():        
        serializer.save()
        return Response({'message': "user created"}, status=status.HTTP_200_OK)
        

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({'message': f'Hello {request.user.username}, you are authenticated!'})