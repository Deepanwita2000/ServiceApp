from django.db import models
from bookings.models import Booking
from accountapp.models import User
from provider.models import Provider
# Create your models here.
class Rating(models.Model):
    booking =models.ForeignKey(Booking , on_delete=models.CASCADE , related_name='rating')
    provider = models.ForeignKey(Provider , on_delete=models.CASCADE , related_name='rating') # read only
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='rating') # read only
    stars = models.IntegerField()
    comment = models.TextField()
    rated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("booking", "user")  # prevent duplicate ratings per booking

    def __str__(self):
        return f"{self.stars}"
    

    # service = models.ForeignKey(Service , on_delete=models.CASCADE , related_name='bookings')
    # catagory = models.ForeignKey(Catagory , on_delete=models.CASCADE , related_name='bookings')


#     from rest_framework import serializers
# from .models import Rating, Booking

# class RatingSerializer(serializers.ModelSerializer):
#     provider = serializers.PrimaryKeyRelatedField(read_only=True)
#     user = serializers.PrimaryKeyRelatedField(read_only=True)
#     booking = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = Rating
#         fields = ["id", "booking", "provider", "user", "stars", "comment", "rated_at"]

#     def create(self, validated_data):
#         request = self.context["request"]
#         booking = self.context["booking"]

#         # Ensure booking is completed before rating
#         if booking.status != "completed":
#             raise serializers.ValidationError("You can only rate after service is completed.")

#         return Rating.objects.create(
#             booking=booking,
#             provider=booking.provider,
#             user=request.user,
#             **validated_data
#         )