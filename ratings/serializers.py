from rest_framework import serializers
from .models import Rating
# class RatingSerializer(serializers.ModelSerializer):
#     provider = serializers.PrimaryKeyRelatedField(read_only=True)
#     user = serializers.PrimaryKeyRelatedField(read_only=True)
#     booking = serializers.PrimaryKeyRelatedField(read_only=True)
#     # booking_id = serializers.PrimaryKeyRelatedField(source='booking', read_only=True)

#     class Meta:
#         model = Rating
#         fields = ["id", "booking", "provider", "user", "stars", "comment", "rated_at"]

#     def create(self, validated_data):
#         request = self.context["request"]
#         booking = self.context.get("booking")   # <-- must be set in view

#         if not booking:
#             raise serializers.ValidationError("Booking is required for rating.")

#         if booking.status != "completed":
#             raise serializers.ValidationError("You can only rate after service is completed.")

#         return Rating.objects.create(
#             booking=booking,
#             provider=booking.provider,
#             user=booking.customer,   # since your Booking has 'customer' not 'user'
#             **validated_data
#         )

    # def create(self, validated_data):
    #     request = self.context["request"]
    #     booking = self.context["booking"]

    #     if booking.status != "completed":
    #         raise serializers.ValidationError("You can only rate after service is completed.")

    #     return Rating.objects.create(
    #         booking=booking,
    #         provider=booking.provider,
    #         user=request.user,
    #         **validated_data
    #     )



class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "booking", "provider", "user", "stars", "comment", "rated_at"]
        read_only_fields = ["id", "provider", "user", "rated_at","booking"]

    def create(self, validated_data):
        # get booking from context
        booking = self.context.get("booking")
        request = self.context.get("request")

        # set user and provider automatically
        validated_data["user"] = request.user
        validated_data["provider"] = booking.provider
        validated_data["booking"] = booking

        return super().create(validated_data)