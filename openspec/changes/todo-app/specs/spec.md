# TODO App Specification

## Overview
The application should allow users to manage TODO tasks.

## Requirements

### Add Task
Users should be able to create a new task with a title.

### Get Tasks
Users should be able to view all tasks.

### Complete Task
Users should be able to mark a task as completed.

### Delete Task
Users should be able to remove a task.

## Technical Notes
- Use FastAPI
- Use in-memory storage
- Keep implementation beginner friendly

## Data Model (Task)

The application manages tasks with the following fields:

* `id` (integer): Unique identifier for the task.
* `title` (string): The task description (created by the user).
* `completed` (boolean): Whether the task is done.

## API Contract

All endpoints are rooted under `/tasks` (except the frontend UI at `/`).

### Add Task

* `POST /tasks`
* Request body (JSON):
  * `title` (string)
* Response (JSON, 201):
  * returns the created `Task` with an auto-generated `id`
  * `completed` starts as `false`

Example request:

```bash
curl -X POST http://localhost:8000/tasks ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"Buy milk\"}"
```

### Get Tasks

* `GET /tasks`
* Response (JSON, 200):
  * an array of `Task` objects

### Complete Task

* `PATCH /tasks/{task_id}/complete`
* Response (JSON, 200):
  * returns the updated `Task` with `completed: true`

If the task id does not exist, the API should return `404`.

### Delete Task

* `DELETE /tasks/{task_id}`
* Response (HTTP 204):
  * no content

If the task id does not exist, the API should return `404`.

## Frontend UI (Simple)

The homepage route `/` should serve a small HTML page (plain HTML/CSS/JS, no React).

The UI should:
* show a form/input to create a new task (title),
* fetch and display the current task list,
* call the complete endpoint when the user marks a task done,
* call the delete endpoint when the user removes a task.

## Storage Behavior

Tasks are stored in memory (a Python list / data structure inside the process).
Restarting the server resets the tasks back to an empty list.
