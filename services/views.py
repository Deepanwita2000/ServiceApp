import os
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404
from django.template.loader import render_to_string
from django.db.models.query import QuerySet


#---------- for drf -------------#
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ServiceApp import settings

from .serializers import ServiceSerializer
from .models import Service





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

from accountapp.authentication import JWTAuthentication, create_access_token, create_refresh_token
from accountapp.models import User, UserToken
from accountapp.permissions import IsCustomer,IsProvider,IsProviderOrCustomerOrAdmin ,IsAdmin
from accountapp.serializers import  UserSerializer


#////////////////////////////////////////////////////////////////////////////  for ADMIN panel  //////////////////////////////////////////////////////////////////////////////////////

def view_service(request):
    services = Service.objects.all()
    print(services)
    return render(request , 'services/add_service.html',{"services":services , "initial_load":True})

def add_service(request):
    if request.method == "POST":
        name = request.POST.get("service_name")
        description = request.POST.get("description")
        icon = request.FILES.get("icon")
        if name and description:
            if not Service.objects.filter(name=name).exists():
                 # create table
                 Service.objects.create(
                     name = name,
                     description = description,
                     icon = icon
                 )

                 # fectch all data from db
                 services = Service.objects.all()
                 html_data = render_to_string('partials/service_rows.html' , {"services":services})
                 return JsonResponse({"message":"Added successfully!!" , "services":html_data})

            else:

                return JsonResponse({"message":f"{name} Already exists!!"} , status=400)
        else:
            return JsonResponse({"message":"All fields are mandatory!!"} , status=400)
    
    else:
        return render(request , 'services/add_service.html')

def edit_service(request , pk=None):
    service_info = get_object_or_404(Service , ifd=pk) if pk else None
    if request.method == "POST":
        name = request.POST.get("service_name")
        description = request.POST.get("description")
        new_icon = request.FILES.get("icon")
        if name and description:
            if not Service.objects.filter(name=name).exclude(id = service_info.id).exists():
                 # save table
                service_info.name = name,
                service_info.description = description,
                if new_icon:
                    # Delete old icon if exists
                    if service_info.icon and os.path.isfile(service_info.icon.path):
                        os.remove(service_info.icon.path)
                    # assign new icon
                    service_info.icon = new_icon
                service_info.save()
                
                   # fectch all data from db
                services = Service.objects.all()
                html_data = render_to_string('partials/service_rows.html' , {"services":services})
                return JsonResponse({"message":"Added successfully!!" , "services":html_data})

            else:

                return JsonResponse({"message":f"{name} Already exists!!"} , status=400)
        else:
            return JsonResponse({"message":"All fields are mandatory!!"} , status=400)

def delete_service(request, service_id=None):
    servive_info = get_object_or_404(Service, pk=service_id)
    print("names : ",servive_info.icon , "servive_info.name: ",servive_info.icon.name)
    # Delete the image file from storage if it exists
    if servive_info.icon and servive_info.icon.name:  # Ensure it has a file
        image_path = os.path.join(settings.MEDIA_ROOT, servive_info.icon.name)
        if os.path.exists(image_path):
            os.remove(image_path)
            
    servive_info.delete()
    # After deletion, return the updated list of streams
    services: QuerySet = Service.objects.all()
    html_string = render_to_string("partials/service_rows.html", {"services": services})
    return JsonResponse({"services": html_string, "message": "service deleted successfully!!"})

# /////////////////////////////////////////////////////////////////////////////////// Class Based View /////////////////////////////////////////////////////

class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    #create service
    def perform_create(self, serializer):
        user = self.request.user            # ModelViewSet → GenericViewSet → APIView that has request.user & request.data
        if user.role != 'admin':        # Only admin can create
            raise PermissionDenied("Only admin can create services.")
        
        # Prevent duplicate service name
        name = serializer.validated_data.get('name')
        print(f'Creating service with title: {name} for user: {user}')

        if Service.objects.filter(name=name, admin=user).exists():
            raise exceptions.ValidationError("Service with this name already exists for this admin.")
        serializer.save(admin=user)


    # Edit a service - Only the professor who created it
    def perform_update(self, serializer):
        service = self.get_object()      # This will get the service instance being updated from queryset = Service.objects.all() 
        user = self.request.user

        print(f'User details: {user}')

        if user.role != 'admin':
            raise PermissionDenied("Only admin can update the service")
        serializer.save()

        # delete service
    def perform_destroy(self, instance):
        user = self.request.user

        # Only admin can delete
        if user.role != 'admin':
            raise PermissionDenied("Only admins can delete services.")

        # (optional) Only the same admin who created the service can delete it
        if instance.admin != user:
            raise PermissionDenied("You can only delete services you created.")

        instance.delete()

    
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Service deleted successfully."}, 
            status=status.HTTP_204_NO_CONTENT
        )
    

    #List services created by the specific authenticated admin
    @action(detail=False, methods=['get'], url_path='my_services_list', permission_classes=[IsAdmin])
    def my_services_list(self, request):
        user = request.user
        if user.role != 'admin':
            raise PermissionDenied("Only admins can access their own services.")

        all_services = Service.objects.filter(admin=user)
        serializer = self.get_serializer(all_services, many=True)
        return Response(serializer.data)
