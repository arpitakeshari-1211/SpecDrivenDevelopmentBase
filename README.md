# Spec Driven Development - Todo App

## What is SDD?

Spec Driven Development means writing the spec first, then implementing based on that spec.  
The spec defines exactly what to build before any code is written.

---

## What I Built

Built a **Todo App** using the OpenSpec SDD workflow.

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

## SDD Process I Followed

### Step 1 - Propose

Used `/opsx:propose` to generate spec artifacts:

- `proposal.md` — what and why
- `tasks.md` — atomic tasks
- `spec.md` — detailed specification

### Step 2 - Review

Read all spec files before touching any code.

### Step 3 - Implement

Used `/opsx:apply` to implement based on the spec.

### Step 4 - Archive

Used `/opsx:archive` to save the spec permanently.

---

## OpenSpec Files

```text
openspec/
└── changes/
    └── todo-app/
        ├── proposal.md
        ├── tasks.md
        └── specs/
            └── spec.md
```

---

## Why SDD is Better than Vibe Coding

- Clear requirements before coding
- No surprises during implementation
- Permanent audit trail
- Easier to maintain and extend

---

## Tech Stack

- Python
- FastAPI
- Pydantic
- OpenSpec

---

## Run

```bash
uvicorn app.main:app --reload --port 8000
```