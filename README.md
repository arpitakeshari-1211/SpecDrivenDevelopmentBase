# Vibe Coded Todo App

## What is Vibe Coding?

Vibe coding means giving a casual prompt to an AI and accepting whatever it builds.  
No planning, no spec, no structure — just prompt and ship!

---

## What I Built

Added a **Todo App** to the existing Reports API.

---

## Features

- Add a task
- List all tasks
- Mark task as completed
- Delete a task

---

## Endpoints

| Method | Path | Description |
|---|---|---|
| POST | /tasks | Add a new task |
| GET | /tasks | List all tasks |
| PATCH | /tasks/{id}/complete | Mark task completed |
| DELETE | /tasks/{id} | Delete a task |

---

## How I Built It

1. Opened Cursor AI
2. Typed a casual prompt describing what I wanted
3. Accepted whatever Cursor generated
4. Ran the app and it worked

---

## What Could Go Wrong with Vibe Coding

- No spec means no clear requirements
- AI might make unexpected decisions
- Hard to maintain or extend later
- No documentation of why things were built a certain way

---

## Tech Stack

- Python
- FastAPI
- Pydantic

---

## Run

```bash
uvicorn app.main:app --reload --port 8000
```