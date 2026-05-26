# Tasks



- [x] Create TODO task model

- [x] Create API routes

- [x] Implement in-memory task storage

- [x] Add create task endpoint

- [x] Add get tasks endpoint

- [x] Add delete task endpoint

- [x] Add complete task feature

- [x] Add simple frontend UI

## Definition of Done
Each checklist item above is considered “done” when:

* The FastAPI endpoint exists and returns the expected JSON shape (when applicable).
* The in-memory storage correctly creates, lists, updates (complete), and deletes tasks.
* The simple frontend UI at `/` can:
  * add a task,
  * display tasks,
  * mark tasks completed,
  * and delete tasks,
  using the TODO API endpoints.

## Quick Acceptance Checks (manual)
From the browser:
* Open `http://localhost:8000/` and verify you can add/complete/delete tasks.

From the API:
* `POST /tasks` with `{"title": "Buy milk"}` returns a task with `id`, `title`, `completed`.
* `GET /tasks` lists tasks.
* `PATCH /tasks/{id}/complete` sets `completed` to `true`.
* `DELETE /tasks/{id}` removes the task.


