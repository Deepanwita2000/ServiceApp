from rest_framework import serializers
from accountapp.models import User
from provider.models import Provider
from .models import Booking
from services.models import Service

class BookingSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(write_only=True) #user_name
    provider_id = serializers.PrimaryKeyRelatedField(source='provider' , read_only=True) #user_id
    provider= serializers.StringRelatedField(read_only=True) #user

    service_name = serializers.CharField(write_only=True)
    service_id = serializers.PrimaryKeyRelatedField(source='service' , read_only=True)
    service= serializers.StringRelatedField(read_only=True)
      
    # catagory_name = serializers.CharField(write_only=True , read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Booking
        fields = ['id', 'user', 'service', 'service_id', 'service_name' ,'catagory_name', 'scheduled_date','scheduled_time' , 'status',
                  "provider_name","provider_id","provider"] 
   
    def create(self, validated_data):
        print(validated_data)
        service_name = validated_data.pop('service_name') # Extracting the stream_name from JSON and removing it as well
        provider_name = validated_data.pop('provider_name') # Extracting the stream_name from JSON and removing it as well
        
        #serch provider profile
        split_names=provider_name.split(" ")
        fname=split_names[0]
        lname=split_names[1]
        try:
            user = User.objects.get(first_name=fname , last_name=lname)
            if user.role != 'provider':
                raise serializers.ValidationError({'user':'user can only choose providers'})
        except User.DoesNotExist:
            raise serializers.ValidationError({'User': 'User not found.'})
        user_id = user.id     
        
        provider_id = Provider.objects.get(provider=user_id)
        # print(service_name)
        # print(validated_data)
        try:
            # So whatever stream_name I gave in POST based on that it will search the Stream ID
            service = Service.objects.get(name=service_name) # service instance 'Electrical'   
            
           
        except Service.DoesNotExist:
            raise serializers.ValidationError({'Service': 'Service not found.'})
        
     
        
        booking_info = Booking.objects.create( provider=provider_id, service=service,**validated_data)
        print(booking_info)
        return booking_info



       
