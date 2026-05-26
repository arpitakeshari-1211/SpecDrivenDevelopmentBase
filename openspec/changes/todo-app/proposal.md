# Proposal: TODO App (FastAPI + OpenSpec)

## Goal
Build a beginner-friendly TODO application using **FastAPI**, driven by the **OpenSpec** workflow in this repository (`openspec/changes/todo-app/`).

The app should let users:
1. Add new tasks (title only)
2. View all tasks
3. Mark a task as completed
4. Delete a task

## Why this change?
This workshop feature demonstrates how to go from:
* a short proposal,
* to a task checklist,
* to a concrete specification,
* and finally to a working implementation (API + simple UI).

## User Stories
1. As a user, I can add a task by entering a title.
2. As a user, I can see my list of tasks.
3. As a user, I can mark a task as completed.
4. As a user, I can delete tasks I no longer need.

## Key Technical Decisions
* **FastAPI** for HTTP endpoints.
* **In-memory storage** (a Python list) to keep the code simple.
  * Restarting the server clears tasks.
* The task model includes:
  * `id`
  * `title`
  * `completed`

## Non-goals (keeps this beginner-friendly)
* No database integration
* No authentication/authorization
* No complex filtering/search

## Success Criteria
* The API endpoints described in `specs/spec.md` work end-to-end.
* The simple frontend UI at `/` uses the TODO API correctly.
* The implementation stays readable and easy to follow for beginners.
