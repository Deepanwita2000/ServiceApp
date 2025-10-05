from rest_framework import serializers
from .models import Catagory
from services.models import Service

class CatagorySerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(write_only=True)  # Accept from service name as input inside POST
    service = serializers.StringRelatedField(read_only=True)  # Display service name in response
    service_id = serializers.PrimaryKeyRelatedField(source='service', read_only=True)

    admin = serializers.StringRelatedField(read_only=True)
    image= serializers.ImageField(max_length=None , use_url=True , required=False)

    class Meta:
        model = Catagory
        fields =['id' , 'name' , 'image','service_name' ,'description', 'service' , 'facilities','service_id' , 'price','admin']

    def create(self, validated_data):
        print(validated_data)
        service_name = validated_data.pop('service_name') # Extracting the stream_name from JSON and removing it as well
        print(service_name)
        print(validated_data)
        try:
            # So whatever stream_name I gave in POST based on that it will search the Stream ID
            service_info= Service.objects.get(name=service_name)   
            print((service_info.name , service_info.description))  
        except Service.DoesNotExist:
            raise serializers.ValidationError({'service_name': 'service not found.'})
        
        catagory_info = Catagory.objects.create(service=service_info, **validated_data)
        print(catagory_info)
        return catagory_info
    
    def update(self ,instance,validated_data):
        service_name= validated_data.pop('service_name',None)

        if service_name:
            try:
                service_obj = Service.objects.get(name=service_name)
                instance.service = service_obj
            except Service.DoesNotExist:
                raise serializers.ValidationError({'service_name': 'Service not found.'})

        # update other fields
        for attr , value in validated_data.items():
            setattr(instance , attr , value)
        instance.save()
        return instance




# name
# description
# service
#  facilities
# price
# admin 
    

        #     def update(self, instance, validated_data):
        # stream_name = validated_data.pop('stream_name', None)  # Optional during PATCH
        # if stream_name:
        #     try:
        #         stream = Stream.objects.get(name=stream_name)
        #         instance.stream = stream
        #     except Stream.DoesNotExist:
        #         raise serializers.ValidationError({'stream_name': 'Stream not found.'})
        
        # # Update other fields like name
        # for attr, value in validated_data.items():
        #     setattr(instance, attr, value)
        
        # instance.save()
        # return instance
    
    

