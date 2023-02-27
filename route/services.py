import random
from typing import Tuple
from rest_framework import exceptions

from route.models import Routes, RouteRequestByUser, RouteRequestContacts


class RouteService:
    __model = Routes
    __rr_model = RouteRequestByUser
    __rr_contact_model = RouteRequestContacts

    @classmethod
    def get_routes(cls, **filters):
        return cls.__model.objects.filter(**filters).order_by("-created_at")

    @classmethod
    def create_route_request(cls, user, route, contact_type, contact_value):
        routeRequest = cls.__rr_model.objects.create(user=user, route_id=route)
        cls.__rr_contact_model.objects.create(
            rr=routeRequest, contact_type=contact_type, contact_value=contact_value
        )

    @classmethod
    def craete_route(
        cls,
        where_from,
        where_to,
        driver,
        price,
        is_open,
        departure_date,
        condition,
    ):
        print(driver)
        route = cls.__model(
            where_from=where_from,
            where_to=where_to,
            driver_id=driver.id,
            price=price,
            is_open=is_open,
            departure_date=departure_date,
            condition=condition,
        )
        route.save()
        return route

    @classmethod
    def get_driver_route_request(cls, user):
        queryset = cls.__rr_model.objects.filter(
            route__driver__user=user, is_deleted=False
        )
        return queryset
