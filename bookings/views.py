import random
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
from provider.models import Provider
from services.models import Service

from .models import Booking
from .serializers import BookingSerializer

# Create your views here.
class UserBookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()             # This will be used for listing and retrieving courses
    serializer_class = BookingSerializer  
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        print(serializer)
        print("-----------------------------------------------------")
        print("------------>>  ",serializer.validated_data)
        user = self.request.user 
        print(f"user -> {user}  ,  user.role -> {user.role}")           # ModelViewSet → GenericViewSet → APIView that has request.user & request.data
        if user.role != 'customer':        # Only professors can create
            raise PermissionDenied("Only customer can book.")
        
        cust_pincode = serializer.validated_data.get('pincode')
        service_name =serializer.validated_data.get('service_name')
        # get service id
        service = Service.objects.get(name=service_name)

        if not Provider.objects.filter(pincode=cust_pincode ,service=service).exists():
            raise PermissionDenied("service is not available in this area")
        else:
            providers=Provider.objects.filter(pincode=cust_pincode ,service=service)        
            provider = random.choice(list(providers))
            print("provider name ->",provider)
        serializer.save(customer=user , provider=provider)

    @action(detail=False, methods=['get'], url_path='my-bookings', permission_classes=[IsCustomer])
    def my_bookings(self,request):
        user = request.user
        if user.role != 'customer':
            raise PermissionDenied("Only customer can access their own courses.")
        
        bookings = Booking.objects.filter(customer=user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)


            # List course created by the specific authenticated professor
    # @action(detail=False, methods=['get'], url_path='my-courses', permission_classes=[IsProfessor])
    # def my_courses(self, request):
    #     user = request.user
    #     if user.role != 'professor':
    #         raise PermissionDenied("Only professors can access their own courses.")

    #     courses = Course.objects.filter(professor=user)
    #     serializer = self.get_serializer(courses, many=True)
    #     return Response(serializer.data)



    #     @action(detail=False , methods=['get'],url_path='my-events' , permission_classes=[IsOrganizer , IsAdmin])
    # def my_events(self, request):
    #     user = request.user
    #     if user.role != 'organizer':
    #         raise PermissionDenied("Only you can see your own created events")
        
    #     all_events = Event.objects.filter(organizer=user)
    #     serializer = self.get_serializer(all_events,many=True)
    #     print(serializer)
    #     return Response(serializer.data)
    
   

