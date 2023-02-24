from django.contrib import admin
from route.models import Routes, RouteRequestByUser, RouteRequestContacts


class RouteRequestInline(admin.StackedInline):
    model = RouteRequestByUser
    fields = [
        "user",
    ]

    extra = 1


@admin.register(Routes)
class RoutesAdmin(admin.ModelAdmin):
    list_display = ("where_from", "where_to", "driver", "price", "is_open")
    list_display_links = (
        "where_from",
        "where_to",
    )
    search_fields = ("where_from", "where_to", "driver", "price")
    list_filter = ("is_open",)
    fields = (
        "where_from",
        "where_to",
        "driver",
        "price",
        "is_open",
        "departure_date",
        "passengers",
        "condition",
        "created_at",
    )
    inlines = [RouteRequestInline]
    readonly_fields = ("created_at",)


class RouteRequestContactsInlines(admin.TabularInline):
    model = RouteRequestContacts
    fields = ["contact_type", "contact_value"]
    extra = 1
    max_num = 5


@admin.register(RouteRequestByUser)
class RoutesRequestAdmin(admin.ModelAdmin):
    list_display = ["route", "user"]
    inlines = [RouteRequestContactsInlines]
