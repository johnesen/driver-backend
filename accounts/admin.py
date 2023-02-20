from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, DriverProfile, ClientProfile
from .forms import UserImageCompressForm
from common.mixins import PhotoTagAdminMixin


@admin.register(User)
class UserAdmin(admin.ModelAdmin, PhotoTagAdminMixin):
    model = User
    list_display = (
        "photo_tag",
        "login",
        "is_active",
        "is_deleted",
    )
    list_display_links = ("login",)
    list_filter = (
        "is_active",
        "is_deleted",
    )
    list_editable = ("is_active", "is_deleted")
    readonly_fields = ("created_at", "updated_at", "password", "last_login")
    search_fields = ("full_name",)
    list_per_page = 25
    form = UserImageCompressForm
    ordering = ["-created_at"]
    PhotoTagAdminMixin.photo_tag.short_description = "Фото"
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "login",
                    "email",
                    "phone",
                    "first_name",
                    "last_name",
                    "middle_name",
                    "code",
                    "password",
                    "photo",
                    "is_active",
                    "is_deleted",
                    "is_driver",
                    "is_client",
                )
            },
        ),
        (
            "Даты",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "last_login",
                )
            },
        ),
    )

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return False


admin.site.unregister(Group)
admin.site.register(DriverProfile)
admin.site.register(ClientProfile)
