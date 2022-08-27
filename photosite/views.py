from rest_framework.response import Response
from rest_framework import permissions, views, status


from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

import datetime

from .models import *
from .serializers import *

# I know most of views could be done in one view but this is more readable for me
# Maybe I will change it later

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
@api_view(['POST'])
@permission_classes((AllowAny,))
def add_message(request):
    fixed_request_data = request.data.copy()
    fixed_request_data.update({'date': datetime.datetime.now()})

    serializer = MessagesSerializer(data=fixed_request_data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET'])
def messages_list(request):
    data = Messages.objects.all()

    serializer = MessagesSerializer(data, context={'request': request}, many=True)

    return Response(serializer.data)

@csrf_exempt
@api_view(['GET'])
def message_details(request, pk):
    try:
        message = Messages.objects.get(pk=pk)
        serializer = MessagesSerializer(message)
        return Response(serializer.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['DELETE'])
def message_delete(request, pk):
    try:
        message = Messages.objects.get(pk=pk)

        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)



# Handle categories
@api_view(["GET"])
@permission_classes((AllowAny,))
def categories_list(request):
    data = Categories.objects.all()

    serializer = CategoriesSerializer(data, context={'request': request}, many=True)

    return Response(serializer.data)

@csrf_exempt
@api_view(["POST"])
def add_category(request):
    serializer = CategoriesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['DELETE'])
def delete_category(request, pk):
    try:
        category = Categories.objects.get(pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['PUT'])
def update_category(request, pk):
    try:
        category = Categories.objects.get(pk=pk)

        serializer = CategoriesSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)