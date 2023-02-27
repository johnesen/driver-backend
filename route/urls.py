from django.urls import path, include
from route.views import *


urlpatterns = [
    path("routes/", RouteListView.as_view(), name="routes-list"),
    path("routes/create/", RouteCreateAPIView.as_view(), name="routes-create"),
    path(
        "routes/send-request/",
        RouteRequestCreateAPIView.as_view(),
        name="routes-request-create",
    ),
    path(
        "driver/routes/request/",
        RequestForDriverListAPIView.as_view(),
        name="route-request-drivers",
    ),
    path(
        "driver/routes/request/<uuid:id>/",
        RouteRequestAcception.as_view(),
        name="route-request-accept-drivers",
    ),
]
