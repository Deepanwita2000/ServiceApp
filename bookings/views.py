from django.shortcuts import render
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

from accountapp.authentication import JWTAuthentication

from accountapp.permissions import IsCustomer


from .models import Booking
from .serializers import BookingSerializer

# Create your views here.
class UserBookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()             # This will be used for listing and retrieving courses
    serializer_class = BookingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        user = self.request.user            # ModelViewSet → GenericViewSet → APIView that has request.user & request.data
        if user.role != 'customer':        # Only professors can create
            raise PermissionDenied("Only customer can book.")
       
        serializer.save(user=user)

