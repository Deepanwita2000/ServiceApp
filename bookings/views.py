import random
# from django.forms import ValidationError
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
from rest_framework import status

from django.utils import timezone
from datetime import timedelta
from rest_framework.exceptions import ValidationError

from accountapp.authentication import JWTAuthentication

from accountapp.models import User
from accountapp.permissions import IsCustomer
from provider.models import Provider
from ratings.serializers import RatingSerializer
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
        print(f"user -> {user}  ,  user.role -> {user.role} , user.contact ->{user.contact}" )           # ModelViewSet → GenericViewSet → APIView that has request.user & request.data
        user_contact = user.contact
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
            provider = random.choice(list(providers)) # provider - instance  of Provider class
            print("provider name ->",provider)
            split_provider = str(provider).split("-")  # ['Electrical', 'peter@gmail.com']
            print(split_provider ,split_provider[1] )
            provider_email = split_provider[1]

            provider_info = User.objects.get(email=provider_email)  # search provider profile
            print(provider_info , provider_info.contact , provider_info.address)
            contact = provider_info.contact
            address =  provider_info.address
            print("provider_info :",provider_info.address , provider_info.contact)

        serializer.save(
                            customer=user , provider=provider , 
                            provider_contact = contact,
                            customer_contact = user_contact,
                            customer_address = address
                        )
        
        return Response({
            "message":"booked sucessfully"
        })
    

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "Booked successfully!"},
            status=status.HTTP_201_CREATED
        )
        # return Response(
        #     {"message": "Booked!", "data": response.data},
        #     status=status.HTTP_201_CREATED
        # )

    @action(detail=False, methods=['get'], url_path='my-bookings', permission_classes=[IsCustomer])
    def my_bookings(self,request):
        user = request.user
        if user.role != 'customer':
            raise PermissionDenied("Only customer can access their own courses.")
        
        bookings = Booking.objects.filter(customer=user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)


   # give ratings by user after service done
    @action(detail=True, methods=["post"], url_path="rate")
    def rate_booking(self, request, pk=None):
        try:
            booking = Booking.objects.get(pk=pk, customer=request.user)
        except Booking.DoesNotExist:
            raise ValidationError("Invalid booking ID or not your booking.")

        if booking.status != "completed":
            raise ValidationError("You can only rate after service is completed.")

        if hasattr(booking, "rating") and booking.rating.exists():
            raise ValidationError("This booking has already been rated.")

        serializer = RatingSerializer(
            data=request.data,
            context={"request": request, "booking": booking}
        )
        serializer.is_valid(raise_exception=True)
        rating = serializer.save()

        return Response(RatingSerializer(rating).data, status=201)

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
    
   

