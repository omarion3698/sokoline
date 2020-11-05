from rest_framework import generics, permissions, serializers, exceptions
from django.contrib.auth.models import User
from . import models
from django.contrib.auth import authenticate
# from .models import Profile

# User Serializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        
# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['id', 'designation', 'picture']
        
# Register Serializer
 
class UserProfileSerializer(serializers.ModelSerializer):
    """A serializer for our user profile objects."""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create and return a new user."""

        user = models.UserProfile(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
    

# class PurchasedProductsList(generics.ListAPIView):
#     """
#     Return a list of all the products that the authenticated
#     user has ever purchased, with optional filtering.
#     """
#     # model = models.Product
#     serializer_class = ProductSerializer
#     filterset_class = ProductFilter

#     def get_queryset(self):
#         user = self.request.user
#         return user.purchase_set.all()
        


