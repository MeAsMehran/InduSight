# drf:
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# models:
from .models import CustomUser

# Tokens:
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

# permissions:
from rest_framework.permissions import IsAuthenticated
from core.permissions.is_super_user import IsSuperUser
from core.permissions.is_admin_user import IsAdminUser
from core.permissions.is_supervisor_user import IsSupervisorUser
from core.permissions.is_not_authenticated import IsNotAuthenticated

# Serializers:
from .serializers import CustomUserRegisterSerializer, CustomUserLoginSerializer, UserSerializer, CustomUserLogoutSerializer


# Create your views here.

class UserRegisterAPIView(APIView):
    # permission_classes = [IsAdminUser]
    serializer_class = CustomUserRegisterSerializer

    @swagger_auto_schema(request_body=CustomUserRegisterSerializer)
    def post(self, request):
        serializer = CustomUserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    permission_classes = [IsNotAuthenticated]
    serializer_class = CustomUserLoginSerializer

    @swagger_auto_schema(request_body=CustomUserLoginSerializer)
    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh'],
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING)
            }
        ),
        responses={205: "Logout successful"}
    )
    def post(self, request):
        
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # This will invalidate the token
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

class CreateUserAPIView(CreateAPIView):
    permission_class = [IsAdminUser]
    serializer_class = CustomUserRegisterSerializer
    


class UpdateUserAPIView(UpdateAPIView):
    permission_class = [IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegisterSerializer
    
    
class DetailUserAPIView(RetrieveAPIView):
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
    
class UserListsAPIView(ListAPIView):
    permission_class = [IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

