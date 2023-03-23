from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.Serializer import RegistrationSerializer, LoginSerializer


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
                            status=status.HTTP_200_OK)


def login_user(request):
    if request.method == 'GET':
        return render(request, "login.html")
    elif request.method == 'POST':
        print(request.POST)
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('index')
        return render(request, "login.html")


