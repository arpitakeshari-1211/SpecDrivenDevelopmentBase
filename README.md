# Reports API

A small FastAPI service that exposes a paginated `/reports` endpoint backed by a deterministic in-memory dataset.

## Layout

```
app/
├── __init__.py
├── data.py          # Seed dataset (120 rows, deterministic)
├── models.py        # Pydantic models — internal vs public
├── reports.py       # Filter / sort / pagination query layer
├── todo_models.py   # Task Pydantic models
├── todo_store.py    # In-memory task storage
├── todo_routes.py   # TODO JSON API (/tasks)
├── todo_ui.py       # Simple HTML homepage (/)
└── main.py          # FastAPI app (reports + todos)
```

## Requirements

- Python 3.10+
- pip

## Setup

```bash
git clone https://github.com/IITMBSMLOps/SpecDrivenDevelopmentBase.git
cd SpecDrivenDevelopmentBase

python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -e .
```

## Run the API

```bash
uvicorn app.main:app --reload --port 8000
```

Then open the TODO UI in your browser:

**http://localhost:8000/**

Or hit the API from another terminal:

```bash
curl "http://localhost:8000/health"
curl "http://localhost:8000/reports?limit=3" | python -m json.tool
```

## Endpoints

| Method | Path       | Description                                            |
| ------ | ---------- | ------------------------------------------------------ |
| GET    | `/health`  | Liveness probe — returns `{"status": "ok"}`.           |
| GET    | `/reports` | Paginated list of reports with filtering and sorting.  |

### TODO API (`/tasks`)

In-memory todo list. Data is lost when the server restarts.

| Method | Path                      | Description              |
| ------ | ------------------------- | ------------------------ |
| POST   | `/tasks`                  | Add a task (`{"title": "..."}`). |
| GET    | `/tasks`                  | List all tasks.          |
| DELETE | `/tasks/{task_id}`        | Delete a task by id.     |
| PATCH  | `/tasks/{task_id}/complete` | Mark a task completed. |

```bash
curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"title\": \"Learn FastAPI\"}"
curl http://localhost:8000/tasks
curl -X PATCH http://localhost:8000/tasks/1/complete
curl -X DELETE http://localhost:8000/tasks/1
```

Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### `GET /reports` query parameters

| Param        | Type            | Default      | Notes                                            |
| ------------ | --------------- | ------------ | ------------------------------------------------ |
| `status`     | enum            | —            | One of `pending`, `approved`, `rejected`, `archived`. |
| `date_from`  | datetime (ISO)  | —            | Lower bound on `created_at` (inclusive).         |
| `date_to`    | datetime (ISO)  | —            | Upper bound on `created_at` (inclusive).         |
| `sort`       | string          | `created_at` | One of `id`, `title`, `status`, `owner`, `amount`, `created_at`. |
| `descending` | bool            | `true`       | Sort direction.                                  |
| `offset`     | int (>=0)       | `0`          | Pagination offset.                               |
| `limit`      | int (1..200)    | `20`         | Page size.                                       |

