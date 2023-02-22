from rest_framework.response import Response
from rest_framework import status, generics, permissions

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
