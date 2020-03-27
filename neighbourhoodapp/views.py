from rest_framework import generics, status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView

from .models import Neighbourhood, Profile, Business, Post, NeighbourhoodAdmin, SystemAdmin, Contact
from .serializer import NeighbourhoodSerializer, ProfileSerializer, BusinessSerializer, PostSerializer, \
    HoodAdminSerializer, UserSerializer, ContactSerializer


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()

    def post(self, request, ):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DeleteUser(generics.DestroyAPIView):
    def destroy(self, request, *args, **kwargs):
        system_admin = SystemAdmin.objects.get(pk=self.kwargs["id"])
        if system_admin.is_admin:
            try:
                queryset = User.objects.get(pk=self.kwargs["pk"])
            except ObjectDoesNotExist:
                return Response({"User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            queryset.delete()
            return Response({"User deleted"})

        else:
            return Response({"Not authorized"}, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(generics.RetrieveUpdateAPIView):
    def get_queryset(self):
        queryset = Profile.objects.filter(user_id=self.kwargs["pk"])
        return queryset

    serializer_class = ProfileSerializer

    def put(self, request, *args, **kwargs):
        profile = Profile.objects.get(pk=self.kwargs["pk"])
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateNeighbourhood(generics.ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        system_admin = SystemAdmin.objects.get(pk=self.kwargs["pk"])
        if system_admin.is_admin:
            name = request.data.get("name")
            location = request.data.get("location")
            occupants_count = request.data.get("occupants_count")
            data = {"name": name, "location": location, "occupants_count": occupants_count}
            serializer = NeighbourhoodSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"Not authorized"}, status=status.HTTP_400_BAD_REQUEST)