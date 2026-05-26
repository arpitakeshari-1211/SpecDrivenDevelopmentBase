# SDD Workshop API

FastAPI project with a **Reports API** and a **TODO app** built from OpenSpec (`openspec/changes/todo-app/`).

## Layout

```
app/
├── __init__.py
├── data.py          # Reports seed dataset
├── models.py        # Reports Pydantic models
├── reports.py       # Reports query layer
├── todo_models.py   # Task model (id, title, completed)
├── todo_store.py    # In-memory task storage
├── todo_routes.py   # TODO JSON API
├── todo_ui.py       # TODO homepage (/)
└── main.py          # FastAPI entrypoint
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

Open the TODO UI: **http://localhost:8000/**

Or use the API from another terminal:

```bash
curl "http://localhost:8000/health"
curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"title\": \"Learn OpenSpec\"}"
curl http://localhost:8000/tasks
curl -X PATCH http://localhost:8000/tasks/1/complete
curl -X DELETE http://localhost:8000/tasks/1
curl "http://localhost:8000/reports?limit=3"
```

## Endpoints

| Method | Path       | Description                                            |
| ------ | ---------- | ------------------------------------------------------ |
| GET    | `/health`  | Liveness probe — returns `{"status": "ok"}`.           |
| GET    | `/reports` | Paginated list of reports with filtering and sorting.  |

### TODO API (in-memory)

| Method | Path | Description |
| ------ | ---- | ----------- |
| GET | `/` | Simple HTML UI |
| POST | `/tasks` | Add task (`{"title": "..."}`) |
| GET | `/tasks` | List all tasks |
| PATCH | `/tasks/{id}/complete` | Mark task completed |
| DELETE | `/tasks/{id}` | Delete task |

API docs: http://localhost:8000/docs

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

