from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from django.template.loader import render_to_string

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from provider.models import Provider
from services.models import Service

from .serializers import ProviderSerializer



from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from accountapp.authentication import JWTAuthentication, create_access_token, create_refresh_token
from accountapp.models import User, UserToken
from accountapp.permissions import IsCustomer,IsProvider,IsProviderOrCustomerOrAdmin
from accountapp.serializers import  UserSerializer


class ProviderRegistrationSet(ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # register as provider
    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'provider':
            raise PermissionDenied("Only provider can register for services !")
        print(serializer.validated_data)
        # prevent duplicate register for service
        service_name = serializer.validated_data.get('service_name')
        service = Service.objects.get(name=service_name)  # sercice name
        print(f"service_id -> {service.id}")
        print(f'Creating servive with title: {service_name} for user : {user}')

        if Provider.objects.filter(service=service.id, provider=user).exists():  # checking if same provider name has registered with same service id
            raise exceptions.ValidationError(f"provider with this service name {service_name} is already registered.")
        serializer.save(provider=user)

    # update registration
    def perform_update(self, serializer):
        provider = self.get_object()  # returns current instance of  model Provider 
        print(provider)
        user = self.request.user
        print(f'User details: {user}')

        if user.role != 'provider' :
            raise PermissionDenied("You can only update your own registration.")
        serializer.save()
    
            # delete service
    def perform_destroy(self, instance):
        user = self.request.user

        if instance.provider != user:
            raise PermissionDenied("You can only delete remove their account.")

        instance.delete()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Service deleted successfully."}, 
            status=status.HTTP_200_OK
        )



