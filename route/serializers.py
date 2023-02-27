from rest_framework import serializers

from accounts.serializers import *
from route.models import Routes, RouteRequestByUser, RouteRequestContacts


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


class RouteRequestContactsSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    contact_type = serializers.CharField(read_only=True)
    contact_value = serializers.CharField(read_only=True)


class RouteRequestSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    user = UserSerializer(read_only=True)
    route = RouteSerializer(read_only=True)
    contacts = RouteRequestContactsSerializer(many=True, read_only=True)
    is_accepted = serializers.BooleanField(read_only=True)


class RouteRequestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteRequestByUser
        fields = ["id", "is_accepted"]

    def update(self, instance, validated_data):
        is_accepted = validated_data.get("is_accepted")
        if is_accepted:
            route = instance.route
            route.passengers.add(instance.user.id)
            route.save()
        return super().update(instance, validated_data)


class RouteRequestCreateSerializer(serializers.Serializer):
    route = serializers.UUIDField(required=True)
    contact_type = serializers.CharField()
    contact_value = serializers.CharField()
