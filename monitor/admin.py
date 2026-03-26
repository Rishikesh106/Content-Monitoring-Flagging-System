from django.contrib import admin

from .models import ContentItem, Flag, Keyword


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(ContentItem)
class ContentItemAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "source", "last_updated")
    search_fields = ("title", "source")
    list_filter = ("source",)


@admin.register(Flag)
class FlagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "keyword",
        "content_item",
        "score",
        "status",
        "reviewed_at",
        "content_snapshot",
    )
    list_filter = ("status", "keyword")
    search_fields = ("keyword__name", "content_item__title")
