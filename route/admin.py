from django.contrib import admin
from route.models import Routes

# Register your models here.
# admin.site.register(Routes)
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
    readonly_fields = ("created_at",)