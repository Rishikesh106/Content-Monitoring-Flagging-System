import re

from django.db import transaction

from .mock_data import MOCK_CONTENT_DATA
from .models import ContentItem, Flag, Keyword


def _seed_mock_content_items():
    for item in MOCK_CONTENT_DATA:
        ContentItem.objects.update_or_create(
            title=item["title"],
            source=item["source"],
            defaults={
                "body": item["body"],
                "last_updated": item["last_updated"],
            },
        )


def _compute_score(keyword_name, content_item):
    title = content_item.title or ""
    body = content_item.body or ""

    escaped = re.escape(keyword_name)
    exact_pattern = re.compile(rf"\b{escaped}\b", re.IGNORECASE)

    if exact_pattern.search(title):
        return 100
    if keyword_name.lower() in title.lower():
        return 70
    if keyword_name.lower() in body.lower():
        return 40
    return None


@transaction.atomic
def run_scan():
    _seed_mock_content_items()

    keywords = list(Keyword.objects.all())
    content_items = list(ContentItem.objects.all())

    flags_created = 0
    flags_updated = 0
    suppressed = 0

    for keyword in keywords:
        for content_item in content_items:
            score = _compute_score(keyword.name, content_item)
            if score is None:
                continue

            flag = Flag.objects.filter(keyword=keyword, content_item=content_item).first()

            if flag:
                if (
                    flag.status == Flag.STATUS_IRRELEVANT
                    and content_item.last_updated == flag.content_snapshot
                ):
                    suppressed += 1
                    continue

                if (
                    flag.status == Flag.STATUS_IRRELEVANT
                    and content_item.last_updated != flag.content_snapshot
                ):
                    flag.score = score
                    flag.status = Flag.STATUS_PENDING
                    flag.content_snapshot = content_item.last_updated
                    flag.save(update_fields=["score", "status", "content_snapshot"])
                    flags_updated += 1
                    continue

                flag.score = score
                flag.save(update_fields=["score"])
                flags_updated += 1
                continue

            Flag.objects.create(
                keyword=keyword,
                content_item=content_item,
                score=score,
                status=Flag.STATUS_PENDING,
                content_snapshot=content_item.last_updated,
            )
            flags_created += 1

    return {
        "flags_created": flags_created,
        "flags_updated": flags_updated,
        "suppressed": suppressed,
    }
