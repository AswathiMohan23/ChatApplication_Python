from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.Serializer import RegistrationSerializer, LoginSerializer
from user.models import UserModel


class UserRegistration(APIView):
    def post(self, request):
        try:
            serializer = RegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message ": "Registration successful", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": e.args[0], "status": 400, "data": {}},
                            status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            return Response({"message": "Login successful", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": e.args[0], "status": 400, "data": {}},
                            status=status.HTTP_400_BAD_REQUEST)


def login_user(request):
    if request.method == 'GET':
        return render(request, "login.html")
    elif request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('index')
        return render(request, "login.html")


def register_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if UserModel.objects.filter(username=username).exists():
            return Response({"message": "user exists", "status": 200, "data": {}},
                            status=status.HTTP_200_OK)
        else:
            UserModel.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                          password=password,
                                          email=email)
            return redirect('login')
    return render(request, "registration.html")
