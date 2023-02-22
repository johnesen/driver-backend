from django.urls import path, include
from route.views import *


urlpatterns = [
    path("routes/", RouteListView.as_view(), name="routes-list"),
    path("routes/create/", RouteCreateAPIView.as_view(), name="routes-create"),
]
