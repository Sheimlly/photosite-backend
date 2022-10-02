import os
from django.conf import settings
from django.core.mail import send_mail

from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

import datetime

from .models import *
from .serializers import *


# Get token
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)



# Handle messages
@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def add_message(request):
    fixed_request_data = request.data.copy()
    fixed_request_data.update({'date': datetime.datetime.now()})

    serializer = MessagesSerializer(data=fixed_request_data)
    serializer = MessagesSerializer(data=fixed_request_data)
    if serializer.is_valid():
        print(settings.EMAIL_HOST_USER)
        phone = f"Nr. Telefonu: {request.data.get('phone')}" if request.data.get('phone') else ""
        message = f"""
            Imię: {request.data.get('name')}
            Email: {request.data.get('email')}
            {phone}
            {request.data.get('message')}
        """
        send_mail(
            subject='Wiadomość z formularza na stronie',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER]
        )
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def messages_list(request):
    data = Messages.objects.all().order_by("-message_id")

    serializer = MessagesSerializer(data, context={'request': request}, many=True)

    return Response(serializer.data)

@csrf_exempt
@api_view(['GET', 'DELETE'])
@permission_classes((IsAuthenticated,))
def message_details(request, pk):
    if request.method == 'GET':
        try:
            message = Messages.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        message.readed=True
        message.save()

        serializer = MessagesSerializer(message)
        return Response(serializer.data)

    if request.method == 'DELETE':
        try:
            message = Messages.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Handle categories
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def categories_list(request):
    if request.method == 'GET':
        data = Categories.objects.all()
        serializer = CategoriesSerializer(data, context={'request': request}, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def edit_category(request, pk):
    if request.method == 'PUT':
        try:
            category = Categories.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CategoriesSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        try:
            category = Categories.objects.get(pk=pk)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def edit_category(request, pk):
    if request.method == 'PUT':
        try:
            category = Categories.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CategoriesSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        try:
            category = Categories.objects.get(pk=pk)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)



# Handle offers
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def offers_list(request):
    if request.method == 'GET':
        data = Offers.objects.all()
        offer_serializer = OffersSerializer(data, context={'request': request}, many=True)
        return Response(offer_serializer.data)

    if request.method == 'POST':
        offer_serializer = OffersSerializer(data=request.data)
        if offer_serializer.is_valid():
            offer_serializer.save()
            return Response(offer_serializer.data, status=status.HTTP_201_CREATED)

        return Response(offer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def offer_details(request, pk):
    if request.method == 'GET':
        try: offer = Offers.objects.get(pk=pk)
        except: return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OffersSerializer(offer, context={'request': request}, many=False)
        return Response(serializer.data)

    if request.method == 'DELETE':
        try:
            offer = Offers.objects.get(pk=pk)
            if(offer.photo): os.remove(offer.photo.path)
            offer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        try:
            offer = Offers.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = OffersSerializer(offer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        try:
            offer = Offers.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = OffersSerializer(offer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)