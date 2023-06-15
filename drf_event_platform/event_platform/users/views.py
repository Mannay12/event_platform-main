from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile


class RegisterView(APIView):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role')

        if not username or not password:
            return Response({'message': 'Username and password are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'message': 'Username already exists'},
                            status=status.HTTP_409_CONFLICT)

        user = User.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)

        # Create UserProfile and associate it with the User
        user_profile = UserProfile.objects.create(user=user, role=role)
        user_profile.name = user.username
        user_profile.save()
        token.save()
        return Response({'token': token.key, 'role': user_profile.role}, status=status.HTTP_201_CREATED)


class LoginView(APIView):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not User.objects.filter(username=username).exists():
            return Response({'message': 'Username does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not user.check_password(password):
            return Response({'message': 'Incorrect password'},
                            status=status.HTTP_401_UNAUTHORIZED)

        token = Token.objects.get(user=user)

        return Response({'token': token.key}, status=status.HTTP_200_OK)
