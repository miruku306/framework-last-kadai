from django.contrib import admin
from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    """
    ビデオ管理画面
    """

    list_display = (
        "product_code",
        "title",
        "genre",
        "stock",
        "rented",
        "available_stock",
        "stock_status",
    )

    search_fields = (
        "product_code",
        "title",
    )

    list_filter = ("genre",)

    ordering = ("product_code",)
