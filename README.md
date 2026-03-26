# Content Monitor

Django + Django REST Framework backend for a Content Monitoring & Flagging System.

## Assumptions

- Content is sourced from a local mock dataset in `monitor/mock_data.py`.
- There is no live external content API integration.

## Tech Choices / Trade-offs

- No authentication is implemented to keep the demo focused on scanning and review logic.
- SQLite is used for simple local setup.
- Scans run synchronously through an API call (no Celery/background worker).

## Setup

1. Create and activate a virtual environment.
2. Install dependencies.
3. Run migrations.
4. Start the dev server.

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Server runs at http://127.0.0.1:8000/

## API Endpoints

### 1. Create Keyword

- Method: POST
- URL: `/api/keywords/`
- Body: `{ "name": "python" }`

```bash
curl -X POST http://127.0.0.1:8000/api/keywords/ \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"python\"}"
```

You can create additional keywords such as `django`, `automation`, and `data pipeline`.

### 2. Run Scan

- Method: POST
- URL: `/api/scan/`
- Body: none

```bash
curl -X POST http://127.0.0.1:8000/api/scan/ \
  -H "Content-Type: application/json"
```

Example response:

```json
{
  "flags_created": 4,
  "flags_updated": 2,
  "suppressed": 1
}
```

### 3. List Flags

- Method: GET
- URL: `/api/flags/`
- Optional query filter: `?status=pending|relevant|irrelevant`

```bash
curl http://127.0.0.1:8000/api/flags/
curl http://127.0.0.1:8000/api/flags/?status=pending
```

Each flag response includes keyword and content title fields (`keyword_name`, `content_item_title`) in addition to IDs.

### 4. Update Flag Status

- Method: PATCH
- URL: `/api/flags/<id>/`
- Body: `{ "status": "relevant" }` (or `irrelevant` / `pending`)

```bash
curl -X PATCH http://127.0.0.1:8000/api/flags/1/ \
  -H "Content-Type: application/json" \
  -d "{\"status\":\"irrelevant\"}"
```

When status changes, `reviewed_at` is set to the current timestamp.

## Suppression Logic

`run_scan()` is implemented in `monitor/services.py` and follows these rules:

1. For each keyword/content pair, a score is computed:
   - exact full-word match in title (case-insensitive) => 100
   - partial substring match in title (case-insensitive) => 70
   - keyword appears only in body (case-insensitive) => 40
   - no match => no flag created/updated
2. If an existing flag is `irrelevant` and content has not changed (`content_item.last_updated == flag.content_snapshot`), it is suppressed and skipped.
3. If an existing flag is `irrelevant` and content changed (`last_updated != content_snapshot`), flag is reset to `pending`, score is refreshed, and `content_snapshot` is updated.
4. Existing `pending` or `relevant` flags are updated in place with the latest score.
5. Missing flags are created with status `pending` and `content_snapshot = content_item.last_updated`.
