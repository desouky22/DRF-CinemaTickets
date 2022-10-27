from django.http import JsonResponse
from .models import Guest, Movie, Reservation, Post
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins, generics, viewsets
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication,
)

from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from .serializers import (
    GuestSerializer,
    MovieSerializer,
    ReservationSerializer,
    PostSerializer,
)

from .permissions import IsAuthorOrReadOnly


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
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

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
            # self.check_object_permissions(request, guest)
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


class MixinsList(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MixinsPK(
    generics.GenericAPIView,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class GenericsList(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class GenericsPK(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class ViewSetGuest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class ViewSetMovie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ViewSetReservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


# find a movie
@api_view(["GET"])
def find_movie(request, *args, **kwargs):
    movies = Movie.objects.filter(
        movie=request.data["movie"],
        hall=request.data["hall"],
    )

    serializer = MovieSerializer(movies, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_new_reservation(request, *args, **kwargs):
    movie = Movie.objects.get(
        hall=request.data["hall"],
        movie=request.data["movie"],
    )

    guest = Guest()
    guest.name = "Mohammed"
    guest.mobile = "445644564564"
    guest.save()

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()
    serializer = ReservationSerializer(reservation)
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class PostPK(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostList(generics.ListCreateAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
