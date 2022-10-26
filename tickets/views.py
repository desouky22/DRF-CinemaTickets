from mimetypes import guess_all_extensions
from django.http import JsonResponse
from .models import Guest, Movie, Reservation
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer
from tickets import serializers


def no_rest_no_model(request, *args, **kwargs):
    guests = [
        {
            "id": 1,
            "name": "omar",
            "mobile": "01066445323",
        },
        {
            "id": 2,
            "name": "ahmed",
            "mobile": "03143444323",
        },
    ]
    return JsonResponse(guests, safe=False)


def no_rest_from_model(request, *args, **kwargs):
    queryset = Guest.objects.all()
    response = {
        "response": list(queryset.values()),
    }
    return JsonResponse(response, safe=False)


@api_view(["GET", "POST"])
def FBV_List(request, *args, **kwargs):
    if request.method == "GET":
        queryset = Guest.objects.all()
        serializer = GuestSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def FBV_PK(request, *args, **kwargs):
    if request.method == "GET":
        try:
            guest = Guest.objects.get(pk=kwargs["pk"])
            serializer = GuestSerializer(guest)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Guest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == "PUT":
        try:
            guest = Guest.objects.get(pk=kwargs["pk"])
            serializer = GuestSerializer(instance=guest, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        except Guest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == "DELETE":
        try:
            guest = Guest.objects.get(pk=kwargs["pk"])
            guest.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Guest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class GuestList(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Guest.objects.all()
        serializer = GuestSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GuestPK(APIView):
    def get(self, request, *args, **kwargs):
        try:
            guest = Guest.objects.get(pk=kwargs["pk"])
            serializer = GuestSerializer(guest)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Guest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        try:
            guest = Guest.objects.get(pk=kwargs["pk"])
            serializer = GuestSerializer(instance=guest, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        except Guest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        try:
            guest = Guest.objects.get(pk=kwargs["pk"])
            guest.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Guest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
