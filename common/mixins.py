from django.db.models import Q
from django.utils.html import format_html


class PhotoTagAdminMixin:
    def photo_tag(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="80" height="80" '
                'style="object-fit:contain"/>'.format(obj.photo.url)
            )
