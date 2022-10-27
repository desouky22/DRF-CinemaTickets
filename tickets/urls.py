from multiprocessing.resource_tracker import ResourceTracker
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register("guests", views.ViewSetGuest)
router.register("movies", views.ViewSetMovie)
router.register("reservations", views.ViewSetReservation)

urlpatterns = [
    path("no_rest_no_model/", views.no_rest_no_model),
    path("no_rest_from_model/", views.no_rest_from_model),
    path("rest/FBV_List/", views.FBV_List),
    path("rest/FBV_PK/<int:pk>/", views.FBV_PK),
    path("rest/CBV_List/", views.GuestList.as_view()),
    path("rest/CBV_PK/<int:pk>/", views.GuestPK.as_view()),
    path("rest/Mixins_List/", views.MixinsList.as_view()),
    path("rest/Mixins_PK/<int:pk>/", views.MixinsPK.as_view()),
    path("rest/Generics_List/", views.GenericsList.as_view()),
    path("rest/Generics_pk/<int:pk>/", views.GenericsPK.as_view()),
    path("rest/ViewSet/", include(router.urls)),
    path("rest/find_movie/", views.find_movie),
    path("rest/new_reservation/", views.create_new_reservation),
    path(
        "api-token-auth/", obtain_auth_token
    ),  # to obtain the token from the data base from the token model
    path("rest/PostPK/<int:pk>/", views.PostPK.as_view()),
    path("rest/PostList/", views.PostList.as_view()),
]
