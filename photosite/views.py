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

from .models import Message
from .serializers import *

@api_view(['POST'])
def add_message(request):
    fixed_request_data = request.data.copy()
    fixed_request_data.update({'date': datetime.datetime.now()})

    serializer = MessageSerializer(data=fixed_request_data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def messages_list(request):
    data = Message.objects.all()

    serializer = MessageSerializer(data, context={'request': request}, many=True)

    return Response(serializer.data)

@api_view(['DELETE'])
def messages_detail(request, pk):
    try:
        message = Message.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    message.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

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


@api_view(["GET"])
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