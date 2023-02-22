from rest_framework import serializers

from accounts.serializers import *
from route.models import Routes


class RouteSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    where_from = serializers.CharField(read_only=True)
    where_to = serializers.CharField(read_only=True)
    driver = DriverSerializer(read_only=True)
    price = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)
    passengers = UserSerializer(many=True, read_only=True)
    is_open = serializers.BooleanField(read_only=True)
    departure_date = serializers.DateTimeField(read_only=True)
    condition = serializers.CharField(read_only=True)
    is_deleted = serializers.BooleanField(read_only=True)


class RouteModelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routes
        fields = [
            "id",
            "where_from",
            "where_to",
            "driver",
            "price",
            # "passengers",
            "is_open",
            "departure_date",
            "condition",
        ]
