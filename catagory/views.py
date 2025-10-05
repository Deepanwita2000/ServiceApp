from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from django.template.loader import render_to_string

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from catagory.models import Catagory
from services.models import Service

from .serializers import CatagorySerializer


from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated

from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from accountapp.authentication import JWTAuthentication
from accountapp.models import User, UserToken
from accountapp.permissions import IsCustomer,IsProvider,IsProviderOrCustomerOrAdmin ,IsAdmin
from accountapp.serializers import  UserSerializer


class CatagoryViewSet(ModelViewSet):
    queryset = Catagory.objects.all()
    serializer_class = CatagorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # create catagories
    def perform_create(self, serializer):
        user = self.request.user            # ModelViewSet → GenericViewSet → APIView that has request.user & request.data
        if user.role != 'admin':        # Only admin can create
            raise PermissionDenied("Only admin can create catagories.")
        
    # Prevent duplicate service name
        service_name = serializer.validated_data.get('service_name')
        print(f'Creating service with title: {service_name} for user: {user}')

        print(service_name)

        service_obj = Service.objects.get(name=service_name)

        # if Catagory.objects.filter(service=service_obj.id, admin=user).exists():
        #     raise exceptions.ValidationError("Service with this name already exists for this admin.")
        serializer.save(admin=user)

    # Edit a service_catagory - Only the admin who created it - giving access to the admin to edit
    def perform_update(self, serializer):
        catagory = self.get_object()      # This will get the service instance being updated from queryset = Catagory.objects.all() 
        user = self.request.user

        print(f'User details: {user}')

        if user.role != 'admin':
            raise PermissionDenied("Only admin can edit this catagory")
        serializer.save()

    # delete catagory
    def perform_destroy(self, instance):
        user = self.request.user

        # Only admin can delete
        if user.role != 'admin':
            raise PermissionDenied("Only admins can delete catagory.")

        # (optional) Only the same admin who created the service can delete it
        # if instance.admin != user:
        #     raise PermissionDenied("You can only delete services you created.")

        instance.delete()

    
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Service deleted successfully."}, 
            status=status.HTTP_204_NO_CONTENT
        )
    
    #List services created by the specific authenticated admin
    @action(detail=False, methods=['get'], url_path='my-catagories', permission_classes=[IsAdmin])
    def my_catagories(self, request):
        user = request.user
        if user.role != 'admin':
            raise PermissionDenied("Only admin can access their own catagory.")

        my_catagories_list = Catagory.objects.filter(admin=user)
        serializer = self.get_serializer(my_catagories_list, many=True)
        return Response(serializer.data)


    # View all catagories without authentication
    @action(detail=False, methods=['get'], url_path='all-categories', permission_classes=[AllowAny] , authentication_classes=[])
    def all_categories(self, request):
        all_catagories = Catagory.objects.all()
        serializer = self.get_serializer(all_catagories, many=True)
        return Response(serializer.data)
    
    
    