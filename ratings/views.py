from django.shortcuts import render
# from requests import Response
# from rest_framework import viewsets, permissions
# from rest_framework.exceptions import ValidationError

# from accountapp.permissions import IsCustomer
# from .models import Rating, Booking
# from .serializers import RatingSerializer

# from rest_framework.permissions import IsAuthenticated
# from rest_framework.permissions import AllowAny
# from rest_framework.exceptions import PermissionDenied
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.decorators import action

# class RatingViewSet(viewsets.ModelViewSet):
#     queryset = Rating.objects.all()
#     serializer_class = None
#     permission_classes = [IsAuthenticated]

#     def rate_booking(self, request, pk=None):
#         # ✅ Ensure booking belongs to current user
#         try:
#             booking = Booking.objects.get(pk=pk, customer=request.user)
#         except Booking.DoesNotExist:
#             raise ValidationError("Invalid booking ID or not your booking.")

#         # ✅ Ensure booking is completed
#         if booking.status != "completed":
#             raise ValidationError("You can only rate after service is completed.")

#         # ✅ Prevent duplicate ratings
#         if hasattr(booking, "rating"):
#             raise ValidationError("This booking has already been rated.")

#         # ✅ Validate and save rating
#         serializer = RatingSerializer(
#             data=request.data,
#             context={"request": request, "booking": booking}
#         )
#         serializer.is_valid(raise_exception=True)
#         rating = serializer.save()

#         return Response(RatingSerializer(rating).data, status=201)

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     booking_id = self.request.data.get("booking_id") or self.kwargs.get("booking_id")

    #     if booking_id:
    #         try:
    #             booking = Booking.objects.get(id=booking_id, user=self.request.user)
    #         except Booking.DoesNotExist:
    #             raise ValidationError("Invalid booking ID or not your booking.")
    #         context["booking"] = booking

    #     return context

    # def perform_create(self, serializer):
    #     # serializer.create() already sets user, provider, booking
    #     serializer.save()

    # @action(detail=True, methods=['post'], permission_classes=[IsCustomer])
    # def rating(self, request, pk=None):
    #     course = self.get_object()
    #     student = request.user
    #     # Prevent duplicate enrollment
    #     if Enrollment.objects.filter(course=course, student=student).exists():
    #         return Response({'detail': 'Already enrolled'}, status=400)
    #     Enrollment.objects.create(course=course, student=student)
    # #     return Response({'detail': 'Enrolled successfully'})  
    

    # @action(detail=True, methods=["post"], url_path="rate")
    # def rate_booking(self, request, pk=None):
    #     try:
    #         booking = Booking.objects.get(pk=pk, customer=request.user)
    #     except Booking.DoesNotExist:
    #         raise ValidationError("Invalid booking ID or not your booking.")

    #     if booking.status != "completed":
    #         raise ValidationError("You can only rate after service is completed.")

    #     serializer = RatingSerializer(data=request.data, context={"request": request, "booking": booking})
    #     serializer.is_valid(raise_exception=True)
    #     rating = serializer.save()

    #     return Response(RatingSerializer(rating).data)


# Create your views here.
# class CourseViewSet(ModelViewSet):
#     queryset = Course.objects.all()             # This will be used for listing and retrieving courses
#     serializer_class = CourseSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     # Create a course
#     def perform_create(self, serializer):
#         user = self.request.user            # ModelViewSet → GenericViewSet → APIView that has request.user & request.data
#         if user.role != 'professor':        # Only professors can create
#             raise PermissionDenied("Only professors can create courses.")
        
#         # Prevent duplicate course
#         title = serializer.validated_data.get('title')
#         print(f'Creating course with title: {title} for user: {user}')

#         if Course.objects.filter(title=title, professor=user).exists():
#             raise exceptions.ValidationError("Course with this title already exists for this professor.")
#         serializer.save(professor=user)