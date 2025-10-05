from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from django.utils import timezone
from datetime import timedelta

from accountapp.serializers import UserSerializer
from accountapp.models import User, UserToken
from accountapp.authentication import JWTAuthentication, create_access_token,create_refresh_token
from accountapp.permissions import IsCustomer,IsProvider,IsProviderOrCustomerOrAdmin


# APIView is the base class for all views in Django REST Framework.
# It provides request.data, request.user, request.auth, authentication_classes, permission_classes and methods like .get(), .post()
class RegisterAPIView(APIView):
    permission_classes = [AllowAny] # anyone can access this endpoint
    authentication_classes = []
    
    def post(self, request: Request):
        user = request.data
        print(f'User data received: {user}')
        
        if User.objects.filter(email=user['email']).exists():
            raise exceptions.APIException('Email already exists!')

        if User.objects.filter(username=user['username']).exists():
            raise exceptions.APIException('Username already exists!')

        if user['password'] != user['password_confirm']:
            raise exceptions.APIException('Passwords do not match!')

        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
# User Login with JWT
class LoginAPIView(APIView):
    permission_classes = [AllowAny]  # Anyone can login
    authentication_classes = []  # No authentication required for login

    def post(self, request: Request):
        email = request.data['email']
        password = request.data['password']        

        # Check if user exists
        user = User.objects.filter(email=email).first()
        if user is None:
            raise exceptions.AuthenticationFailed('Invalid credentials')
        
        if user.role == 'provider' and user.is_approved == False:
            raise exceptions.AuthenticationFailed('You are not yet approved!')

        
        # Check if password is correct
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Invalid password')
        
        # Generate access and refresh tokens
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        # Save refresh token of a specific user with an expiration date of 7 days
        UserToken.objects.create(
            user=user, 
            token=refresh_token, 
            expired_at = timezone.now() + timedelta(days=7)
        )
        
        response = Response()
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return response

# Logout User    
class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    def post(self, request: Request):
        refresh_token = request.data.get('refresh_token') or request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'detail': 'Refresh token missing'}, status=400)

        UserToken.objects.filter(token=refresh_token).delete()

        response: Response = Response({
            'status': 'success',
            'message': 'Logged out successfully'
        }, status=200)

        response.delete_cookie(key='refresh_token')
        return response
    
   
# check authenticated user
class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsProviderOrCustomerOrAdmin] 
     
    def get(self,request:Request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(
                {
                    'user':serializer.data,
                    'role': user.role,
                    'is_provider':user.role == 'provider',
                    'is_customer':user.role == 'customer',
                    'is_admin':user.role == 'admin',

                }  )

    





