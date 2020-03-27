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


class SpecificHood(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(pk=self.kwargs["pk"])
        except ObjectDoesNotExist:
            return Response({"Object does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Neighbourhood.objects.get(pk=profile.neighbourhood.id)
        serializer = NeighbourhoodSerializer(queryset)
        if serializer.is_valid:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditHoodInfo(generics.RetrieveUpdateAPIView):
    def get_queryset(self):
        queryset = Neighbourhood.objects.filter(pk=self.kwargs["pk"])
        return queryset

    serializer_class = NeighbourhoodSerializer

    def put(self, request, *args, **kwargs):
        system_admin = SystemAdmin.objects.get(pk=self.kwargs["id"])
        if system_admin.is_admin:
            hood = Neighbourhood.objects.get(pk=self.kwargs["pk"])
            serializer = NeighbourhoodSerializer(hood, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"Not authorized"}, status=status.HTTP_400_BAD_REQUEST)


class DeleteHood(generics.DestroyAPIView):
    def destroy(self, request, *args, **kwargs):
        system_admin = SystemAdmin.objects.get(pk=self.kwargs["id"])
        if system_admin.is_admin:
            try:
                queryset = Neighbourhood.objects.get(pk=self.kwargs["pk"])
            except ObjectDoesNotExist:
                return Response({"Neighbourhood does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            queryset.delete()
            return Response({"Neighbourhood deleted"})

        else:
            return Response({"Not authorized"}, status=status.HTTP_400_BAD_REQUEST)


class HoodBusiness(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset = Business.objects.all()
        return queryset

    serializer_class = BusinessSerializer

    def post(self, request, *args, **kwargs):
        hoodadmin = NeighbourhoodAdmin.objects.get(pk=self.kwargs["pk"])
        system_admin = SystemAdmin.objects.get(pk=self.kwargs["pk"])
        if hoodadmin.is_hood_admin or system_admin.is_admin:
            try:
                profile = Profile.objects.get(pk=self.kwargs["pk"])
            except ObjectDoesNotExist:
                return Response({"Object does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            name = request.data.get("name")
            email = request.data.get("email")
            description = request.data.get("description")
            data = {'name': name, 'email': email, 'description': description, 'neighbourhood': profile.neighbourhood.id}
            serializer = BusinessSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"Not authorized"}, status=status.HTTP_400_BAD_REQUEST)


class BusinessList(generics.ListAPIView):
    def get_queryset(self):
        try:
            profile = Profile.objects.get(pk=self.kwargs["pk"])
        except ObjectDoesNotExist:
            return Response({"Object does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Business.objects.filter(neighbourhood=profile.neighbourhood.id)
        return queryset

    serializer_class = BusinessSerializer


class UpdateBusiness(generics.UpdateAPIView):
    def put(self, request, *args, **kwargs):
        hoodadmin = NeighbourhoodAdmin.objects.get(pk=self.kwargs["pk"])
        system_admin = SystemAdmin.objects.get(pk=self.kwargs["pk"])
        if hoodadmin.is_hood_admin or system_admin.is_admin:
            try:
                profile = Profile.objects.get(pk=self.kwargs["pk"])
            except ObjectDoesNotExist:
                return Response({"Object does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            queryset = Business.objects.get(neighbourhood=profile.neighbourhood.id, name=self.kwargs["name"])
            serializer = BusinessSerializer(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"Not authorized"}, status=status.HTTP_400_BAD_REQUEST)


class Contacts(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        hoodadmin = NeighbourhoodAdmin.objects.get(pk=self.kwargs["pk"])
        system_admin = SystemAdmin.objects.get(pk=self.kwargs["pk"])
        if hoodadmin.is_hood_admin or system_admin.is_admin:
            try:
                profile = Profile.objects.get(pk=self.kwargs["pk"])
            except ObjectDoesNotExist:
                return Response({"Object does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            service_name = request.data.get("service_name")
            phone_no = request.data.get("phone_no")
            location = request.data.get("location")
            data = {'service_name': service_name, 'phone_no': phone_no, 'location': location,
                    'neighbourhood': profile.neighbourhood.id}
            serializer = ContactSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"Not authorized"}, status=status.HTTP_400_BAD_REQUEST)


class ContactList(generics.ListAPIView):
    def get_queryset(self):
        try:
            profile = Profile.objects.get(pk=self.kwargs["pk"])
        except ObjectDoesNotExist:
            return Response({"Object does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Contact.objects.filter(neighbourhood=profile.neighbourhood.id)
        return queryset

    serializer_class = ContactSerializer


class UpdateContacts(generics.UpdateAPIView):
    def put(self, request, *args, **kwargs):
        hoodadmin = NeighbourhoodAdmin.objects.get(pk=self.kwargs["pk"])
        system_admin = SystemAdmin.objects.get(pk=self.kwargs["pk"])
        if hoodadmin.is_hood_admin or system_admin.is_admin:
            try:
                profile = Profile.objects.get(pk=self.kwargs["pk"])
            except ObjectDoesNotExist:
                return Response({"Object does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            queryset = Contact.objects.get(neighbourhood=profile.neighbourhood.id,
                                           service_name=self.kwargs["service_name"])
            serializer = ContactSerializer(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Not authorized"}, status=status.HTTP_400_BAD_REQUEST)