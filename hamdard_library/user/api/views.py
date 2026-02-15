from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import IntegrityError

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
            return Response({'detail': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        tokens = get_tokens_for_user(user=user)
        return Response(tokens, status=status.HTTP_200_OK)

        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response({'detail': "user created"}, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response(
                {"error": "User already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Logout View
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    refresh = request.data.get("refresh")

    if not refresh:
        return Response({"detail": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = RefreshToken(refresh)
        token.blacklist()
        return Response({"detail": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception:
        return Response({"detail": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

# special view just for testing purposes
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({'detail': f'Hello {request.user.username}, you are authenticated!'})

# User Delete View
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    refresh = request.data.get("refresh")
    if refresh:
        token = RefreshToken(refresh)
        token.blacklist()

    user.delete()

    return Response(
        {"detail": "User deleted and logged out"},
        status=status.HTTP_204_NO_CONTENT
    )