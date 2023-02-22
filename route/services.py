import random
from typing import Tuple
from rest_framework import exceptions

from route.models import Routes


class RouteService:
    __model = Routes

    @classmethod
    def get_routes(cls, **filters):
        return cls.__model.objects.filter(**filters).order_by("-created_at")

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
