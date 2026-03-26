from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import ContentItem, Flag, Keyword


class KeywordSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Keyword.objects.all(), message="Keyword must be unique.")]
    )

    class Meta:
        model = Keyword
        fields = ["id", "name"]


class ContentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentItem
        fields = ["id", "title", "source", "body", "last_updated"]


class FlagSerializer(serializers.ModelSerializer):
    keyword_name = serializers.CharField(source="keyword.name", read_only=True)
    content_item_title = serializers.CharField(source="content_item.title", read_only=True)

    class Meta:
        model = Flag
        fields = [
            "id",
            "keyword",
            "keyword_name",
            "content_item",
            "content_item_title",
            "score",
            "status",
            "reviewed_at",
            "content_snapshot",
        ]
        read_only_fields = [
            "keyword",
            "keyword_name",
            "content_item",
            "content_item_title",
            "score",
            "reviewed_at",
            "content_snapshot",
        ]


class FlagStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flag
        fields = ["status"]

    def validate_status(self, value):
        allowed = {choice[0] for choice in Flag.STATUS_CHOICES}
        if value not in allowed:
            raise serializers.ValidationError("Invalid status value.")
        return value
