from django.db import models


class Keyword(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class ContentItem(models.Model):
    title = models.CharField(max_length=500)
    source = models.CharField(max_length=255)
    body = models.TextField()
    last_updated = models.DateTimeField()

    class Meta:
        ordering = ["-last_updated", "title"]

    def __str__(self):
        return f"{self.title} ({self.source})"


class Flag(models.Model):
    STATUS_PENDING = "pending"
    STATUS_RELEVANT = "relevant"
    STATUS_IRRELEVANT = "irrelevant"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_RELEVANT, "Relevant"),
        (STATUS_IRRELEVANT, "Irrelevant"),
    ]

    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name="flags")
    content_item = models.ForeignKey(ContentItem, on_delete=models.CASCADE, related_name="flags")
    score = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    content_snapshot = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["keyword", "content_item"], name="unique_flag_per_keyword_content")
        ]
        ordering = ["-score", "id"]

    def __str__(self):
        return f"{self.keyword.name} -> {self.content_item.title} ({self.status})"
