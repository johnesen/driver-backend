from rest_framework.response import Response
from rest_framework import status, generics, permissions, mixins

from common.permissions import IsDriver

from route.serializers import *
from route.models import *
from route.services import *


class RouteListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RouteSerializer
    queryset = RouteService.get_routes(is_deleted=False)


class RouteCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsDriver]
    serializer_class = RouteModelCreateSerializer
    queryset = RouteService.get_routes(is_deleted=False)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        route = RouteService.craete_route(
            where_from=serializer.validated_data.get("where_from"),
            where_to=serializer.validated_data.get("where_to"),
            driver=request.user.driver,
            price=serializer.validated_data.get("price"),
            is_open=serializer.validated_data.get("is_open"),
            departure_date=serializer.validated_data.get("departure_date"),
            condition=serializer.validated_data.get("conditon"),
        )

        return Response(RouteSerializer(route).data, status=status.HTTP_201_CREATED)


class RouteRequestCreateAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RouteRequestCreateSerializer
    queryset = RouteRequestByUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rr = RouteService.create_route_request(
            user=request.user,
            route=request.data.get("route"),
            contact_type=request.data.get("contact_type"),
            contact_value=request.data.get("contact_value"),
        )
        return Response(RouteRequestSerializer(rr).data, status=status.HTTP_201_CREATED)


class RequestForDriverListAPIView(generics.ListAPIView):
    permission_classes = [IsDriver]
    serializer_class = RouteRequestSerializer

    def get_queryset(self):
        return RouteService.get_driver_route_request(self.request.user)


class RouteRequestAcception(
    mixins.UpdateModelMixin, generics.GenericAPIView
):
    serializer_class = RouteRequestModelSerializer
    queryset = RouteRequestByUser.objects.all()
    permission_classes = [IsDriver]
    lookup_field = "id"

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
