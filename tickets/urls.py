from django.urls import path, include
from . import views

urlpatterns = [
    path("no_rest_no_model/", views.no_rest_no_model),
    path("no_rest_from_model/", views.no_rest_from_model),
    path("rest/FBV_List/", views.FBV_List),
    path("rest/FBV_PK/<int:pk>/", views.FBV_PK),
    path("rest/CBV_List/", views.GuestList.as_view()),
    path("rest/CBV_PK/<int:pk>/", views.GuestPK.as_view()),
]
