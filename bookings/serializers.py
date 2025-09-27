from rest_framework import serializers
from accountapp.models import User
from provider.models import Provider
from .models import Booking
from services.models import Service
from catagory.models import Catagory

from rest_framework.exceptions import PermissionDenied

class BookingSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(write_only=True)
    service_id = serializers.PrimaryKeyRelatedField(source='service' , read_only=True)
    service= serializers.StringRelatedField(read_only=True)
      
    catagory_name = serializers.CharField(write_only=True)
    catagory_id = serializers.PrimaryKeyRelatedField(source='catagory' , read_only=True) 
    catagory = serializers.StringRelatedField(read_only=True)  

    customer = serializers.StringRelatedField(read_only=True)
    provider = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'customer', 'service', 'service_id', 'service_name','catagory','catagory_id' ,'catagory_name','pincode', 'date','time' , 'status',
                  'booked_at','provider'
                  ] 
   
    def create(self, validated_data):
        print(validated_data)
        service_name = validated_data.pop('service_name') # Extracting the stream_name from JSON and removing it as well
        catagory_name = validated_data.pop('catagory_name') # Extracting the stream_name from JSON and removing it as well
        
        try:
            # So whatever stream_name I gave in POST based on that it will search the Stream ID
            service = Service.objects.get(name=service_name) # service instance 'Electrical'   
        except Service.DoesNotExist:
            raise serializers.ValidationError({'Service': 'Service not found.'})
    
        try:
            catagory = Catagory.objects.get(name=catagory_name)
        except Catagory.DoesNotExist:
            raise serializers.ValidationError({'Catagory': 'catagory not found.'})
     
        
        booking_info = Booking.objects.create(catagory=catagory, service=service,**validated_data)
        print(booking_info)
        return booking_info
    
    

    
    # List course created by the specific authenticated professor
    # @action(detail=False, methods=['get'], url_path='my-courses', permission_classes=[IsProfessor])
    # def my_courses(self, request):
    #     user = request.user
    #     if user.role != 'professor':
    #         raise PermissionDenied("Only professors can access their own courses.")

    #     courses = Course.objects.filter(professor=user)
    #     serializer = self.get_serializer(courses, many=True)
    #     return Response(serializer.data)



       
