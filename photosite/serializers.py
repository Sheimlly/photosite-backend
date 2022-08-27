from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *

class MessagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Messages
        fields = ('message_id', 'name', 'phone', 'email', 'message', 'date')
    
    extra_kwargs = {'phone': {'required': False}}


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories 
        fields = ('category_id', 'name', 'active')