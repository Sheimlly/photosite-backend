from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message 
        fields = ('message_id', 'name', 'phone', 'email', 'message', 'date')
    
    extra_kwargs = {'phone': {'required': False}}


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories 
        fields = ('name', 'active')