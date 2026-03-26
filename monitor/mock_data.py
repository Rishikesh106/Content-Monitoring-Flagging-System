from django.utils import timezone


now = timezone.now()

MOCK_CONTENT_DATA = [
    {
        "title": "Python Automation Trends for 2026",
        "body": "Teams are adopting python scripts to automate repetitive operations at scale.",
        "source": "TechPulse",
        "last_updated": now,
    },
    {
        "title": "Django Security Checklist for Enterprise Apps",
        "body": "A practical guide for hardening django deployments in regulated industries.",
        "source": "SecureWeekly",
        "last_updated": now - timezone.timedelta(hours=2),
    },
    {
        "title": "How to Build a Reliable Data Pipeline",
        "body": "This article explores validation, retries, and observability for data pipeline systems.",
        "source": "DataOps Digest",
        "last_updated": now - timezone.timedelta(days=1),
    },
    {
        "title": "Automation in Retail Forecasting",
        "body": "Automation helps planners reduce stockouts and improve replenishment cycles.",
        "source": "Retail AI News",
        "last_updated": now - timezone.timedelta(days=2),
    },
    {
        "title": "Cloud Cost Controls for Growing Startups",
        "body": "Budget alerts and rightsizing recommendations for engineering teams.",
        "source": "Infra Today",
        "last_updated": now - timezone.timedelta(days=3),
    },
    {
        "title": "Data Governance Without Slowing Delivery",
        "body": "Policy-as-code can keep governance aligned with fast-moving data pipeline teams.",
        "source": "Governance Journal",
        "last_updated": now - timezone.timedelta(days=4),
    },
    {
        "title": "Django vs Flask: API Delivery Speed",
        "body": "A benchmark comparing django and flask for CRUD-heavy API projects.",
        "source": "Dev Compare",
        "last_updated": now - timezone.timedelta(days=5),
    },
    {
        "title": "Modern Incident Response Workflows",
        "body": "Runbooks, automation hooks, and timeline reconstruction best practices.",
        "source": "Ops Bulletin",
        "last_updated": now - timezone.timedelta(days=6),
    },
    {
        "title": "Quarterly HR Policy Updates",
        "body": "Internal policy changes for travel, compensation, and onboarding processes.",
        "source": "Internal Memo",
        "last_updated": now - timezone.timedelta(days=7),
    },
    {
        "title": "Python in Education: Classroom Projects",
        "body": "Hands-on python labs improve beginner confidence and problem-solving.",
        "source": "EdTech Review",
        "last_updated": now - timezone.timedelta(days=8),
    },
]
