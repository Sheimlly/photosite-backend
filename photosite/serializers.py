from rest_framework import serializers
from .models import *

class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ('message_id', 'name', 'phone', 'email', 'message', 'date', 'readed')
    
    extra_kwargs = {'phone': {'required': False}}

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('category_id', 'name')


# Offers serializers
class OfferDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDescription
        fields = ('offer_description_id', 'description')

class OffersSerializer(serializers.ModelSerializer):
    descriptions = OfferDescriptionSerializer(source='offer_description', many=True)
    
    class Meta:
        model = Offers
        fields = ('offer_id', 'name', 'price', 'active', 'frontpage', 'photo', 'descriptions')

    extra_kwargs = {'photo': {'required': False}}

    def create(self, validated_data):
        description_data = validated_data.pop('offer_description')
        offer = Offers.objects.create(**validated_data)
        for description_data in description_data:
            OfferDescription.objects.create(offer=offer, **description_data)
        return offer

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.active = validated_data.get('active', instance.active)
        instance.frontpage = validated_data.get('frontpage', instance.frontpage)
        instance.save()

        if(validated_data.get('offer_description')):
            description_data = validated_data.pop('offer_description')
            OfferDescription.objects.filter(offer_id=instance.offer_id).delete()
            for description_data in description_data:
                OfferDescription.objects.create(offer=instance, **description_data)
        
        if(validated_data.get('photo')):
            print(validated_data)
            instance.photo = validated_data.get('photo')
            instance.save()

        return 