from rest_framework import serializers
from .models import Provider
from services.models import Service

from accountapp.models import User

class ProviderSerializer(serializers.ModelSerializer):
    service=serializers.StringRelatedField(read_only=True)
    service_name = serializers.CharField(write_only=True)  # need to write in postman
    service_id = serializers.PrimaryKeyRelatedField(source='service', read_only=True)

    # provider
    provider = serializers.StringRelatedField(read_only=True) 
    # provider_fname = serializers.CharField(write_only=True)
    # provider_lname = serializers.CharField(write_only=True)
    provider_id = serializers.PrimaryKeyRelatedField(source='provider',read_only=True)

    image=serializers.ImageField(max_length=None , use_url=True , required=False)

    class Meta:
        model=Provider
        # fields=['id','service','serviceAreaZip','experience','chargesPerHour','is_available','service_name','service_id','provider','provider_fname','provider_lname','provider_id']
        fields=['id','service','pincode','experience','image','chargesPerHour','service_name','service_id','provider','provider_id','location','is_approved']
    
    def create(self, validate_data):
        service_name = validate_data.pop('service_name')
        # provider_fname = validate_data.pop('provider_fname')
        # provider_lname = validate_data.pop('provider_lname')
        try:
            service = Service.objects.get(name=service_name)
            # provider = User.objects.get(first_name=provider_fname,last_name=provider_lname)
            print(service.name ,service.description )
            

        except Service.DoesNotExist:
            raise serializers.ValidationError({"service_name":f"{service_name} is not available"})
       
        provider_instance = Provider.objects.create(service=service ,**validate_data)
        print(provider_instance)
        return provider_instance
    
    def update(self,instance, validated_data):
        service_name = validated_data.pop('service_name', None)  # Optional during PATCH
        if service_name:
            try:
                service_info = Service.objects.get(name=service_name)
                instance.service = service_info
            except Service.DoesNotExist:
                raise serializers.ValidationError({'service_name': 'service not found.'})
            
        # Update other fields like name
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

