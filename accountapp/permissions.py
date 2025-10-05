from rest_framework.permissions import BasePermission

# Role-based access control (RBAC) permissions is a way to manage authorization
# In RBAC with BasePermission, permissions are implemented through custom logic rather than stored data — 
# and DRF evaluates that logic at runtime to allow or deny access to views.


# Permission to allow provider 
class IsProvider(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'provider'

# Permission to allow only customer to book provider
class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'customer'
    
# permission to allow only for the admin to create services 
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

# User can be either a provider or a customer
# This permission allows both provider and customer to access the view
class IsProviderOrCustomerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role in ['provider', 'customer' , 'admin']
    
