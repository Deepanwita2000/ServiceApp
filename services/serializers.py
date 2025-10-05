import re
from rest_framework import serializers
from services.models import Service

class ServiceSerializer(serializers.ModelSerializer):
    icon =serializers.ImageField(max_length=None , use_url=True , required=False)
    admin = serializers.StringRelatedField(read_only=True)

    

    class Meta:
        model = Service
        fields = ['id', 'name', 'icon','description' , 'admin']

    def validate_name(self , value):
        if str(value).isdigit():
            raise serializers.ValidationError("Name must not be a number")
        pattern = r'^[A-Za-z]+(?: [A-Za-z]+)*$'
        if not bool(re.match(pattern, str(value))):
            raise serializers.ValidationError("Name must contain only letters and space")
        
        if Service.objects.filter(name__iexact = value).exists():
            raise serializers.ValidationError("Service with this name already exists.")
        
        return value

    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError("Description cannot be blank.")
        print(len(value))    
        if len(value) > 200:
            raise serializers.ValidationError("Letters must not exeed more than 200 characters")

        return value


