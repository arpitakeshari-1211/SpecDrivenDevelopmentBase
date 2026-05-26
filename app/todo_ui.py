"""Simple HTML homepage for the TODO app."""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["ui"])

# Single-page UI: inline CSS + vanilla JS calling the JSON API at /tasks.
TODO_PAGE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>TODO List</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
      min-height: 100vh;
      color: #f8fafc;
      padding: clamp(1rem, 4vw, 2.5rem) clamp(0.75rem, 3vw, 1.5rem);
      background: linear-gradient(135deg, #0f172a 0%, #312e81 40%, #7c3aed 75%, #ec4899 100%);
      background-attachment: fixed;
    }

    /* Soft glow behind the main card */
    .page-wrap {
      max-width: 560px;
      margin: 0 auto;
      position: relative;
    }

    .page-wrap::before {
      content: "";
      position: absolute;
      inset: -20% -10% auto;
      height: 200px;
      background: radial-gradient(circle, rgba(255,255,255,0.25), transparent 70%);
      pointer-events: none;
      z-index: 0;
    }

    .glass-card {
      position: relative;
      z-index: 1;
      background: rgba(255, 255, 255, 0.12);
      backdrop-filter: blur(18px);
      -webkit-backdrop-filter: blur(18px);
      border: 1px solid rgba(255, 255, 255, 0.28);
      border-radius: 24px;
      box-shadow:
        0 8px 32px rgba(15, 23, 42, 0.35),
        inset 0 1px 0 rgba(255, 255, 255, 0.35);
      padding: clamp(1.25rem, 4vw, 2rem);
    }

    .header {
      text-align: center;
      margin-bottom: 1.75rem;
    }

    .header-icon {
      font-size: 2.25rem;
      line-height: 1;
      margin-bottom: 0.5rem;
      filter: drop-shadow(0 4px 12px rgba(0,0,0,0.2));
    }

    h1 {
      font-size: clamp(1.35rem, 4vw, 1.75rem);
      font-weight: 700;
      letter-spacing: -0.02em;
      text-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }

    .subtitle {
      margin-top: 0.35rem;
      font-size: 0.9rem;
      color: rgba(248, 250, 252, 0.75);
    }

    .error {
      display: none;
      margin-bottom: 1rem;
      padding: 0.75rem 1rem;
      border-radius: 14px;
      font-size: 0.9rem;
      background: rgba(239, 68, 68, 0.2);
      border: 1px solid rgba(252, 165, 165, 0.45);
      color: #fecaca;
    }

    form {
      display: flex;
      flex-wrap: wrap;
      gap: 0.65rem;
      margin-bottom: 1.5rem;
    }

    input[type="text"] {
      flex: 1 1 180px;
      min-width: 0;
      padding: 0.85rem 1.1rem;
      font-size: 1rem;
      color: #f8fafc;
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.25);
      border-radius: 16px;
      box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.08);
      transition: border-color 0.25s ease, box-shadow 0.25s ease, transform 0.2s ease;
    }

    input[type="text"]::placeholder {
      color: rgba(248, 250, 252, 0.5);
    }

    input[type="text"]:focus {
      outline: none;
      border-color: rgba(196, 181, 253, 0.8);
      box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.35);
      transform: translateY(-1px);
    }

    button {
      padding: 0.85rem 1.25rem;
      border: none;
      border-radius: 16px;
      font-size: 0.95rem;
      font-weight: 600;
      cursor: pointer;
      color: #fff;
      background: linear-gradient(135deg, #6366f1, #8b5cf6);
      border: 1px solid rgba(255, 255, 255, 0.2);
      box-shadow: 0 4px 16px rgba(99, 102, 241, 0.45);
      transition: transform 0.2s ease, box-shadow 0.2s ease, filter 0.2s ease;
    }

    button:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(99, 102, 241, 0.55);
      filter: brightness(1.08);
    }

    button:active {
      transform: translateY(0);
    }

    button.secondary {
      background: rgba(255, 255, 255, 0.15);
      color: #e9d5ff;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      border: 1px solid rgba(255, 255, 255, 0.25);
    }

    button.secondary:hover {
      background: rgba(255, 255, 255, 0.22);
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
    }

    button.danger {
      background: rgba(239, 68, 68, 0.25);
      color: #fecaca;
      box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
      border: 1px solid rgba(252, 165, 165, 0.35);
    }

    button.danger:hover {
      background: rgba(239, 68, 68, 0.4);
      box-shadow: 0 6px 18px rgba(239, 68, 68, 0.35);
    }

    .btn-icon { margin-right: 0.25rem; }

    ul {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }

    li.task-item {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.65rem;
      padding: 1rem 1.1rem;
      border-radius: 18px;
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      box-shadow: 0 4px 16px rgba(15, 23, 42, 0.2);
      transition: transform 0.25s ease, box-shadow 0.25s ease, opacity 0.3s ease;
    }

    li.task-item:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(15, 23, 42, 0.28);
      border-color: rgba(255, 255, 255, 0.35);
    }

    li.task-item.completed {
      opacity: 0.55;
      background: rgba(255, 255, 255, 0.06);
    }

    li.task-item.completed:hover {
      transform: none;
      box-shadow: 0 4px 16px rgba(15, 23, 42, 0.15);
    }

    .task-status {
      font-size: 1.15rem;
      flex-shrink: 0;
      line-height: 1;
    }

    .task-title {
      flex: 1 1 120px;
      min-width: 0;
      word-break: break-word;
      font-size: 1rem;
      line-height: 1.4;
      transition: color 0.3s ease;
    }

    .task-title.done {
      text-decoration: line-through;
      text-decoration-thickness: 2px;
      color: rgba(248, 250, 252, 0.55);
    }

    .actions {
      display: flex;
      flex-wrap: wrap;
      gap: 0.4rem;
      margin-left: auto;
    }

    .actions button {
      padding: 0.5rem 0.85rem;
      font-size: 0.85rem;
      border-radius: 12px;
    }

    .empty {
      text-align: center;
      padding: 2rem 1rem;
      border-radius: 18px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px dashed rgba(255, 255, 255, 0.25);
      color: rgba(248, 250, 252, 0.7);
      font-size: 0.95rem;
      line-height: 1.5;
    }

    .empty-icon {
      display: block;
      font-size: 2rem;
      margin-bottom: 0.5rem;
      opacity: 0.9;
    }

    @media (max-width: 480px) {
      form { flex-direction: column; }
      form button { width: 100%; }
      .actions {
        width: 100%;
        margin-left: 0;
        justify-content: flex-end;
      }
    }
  </style>
</head>
<body>
  <div class="page-wrap">
    <div class="glass-card">
      <header class="header">
        <div class="header-icon" aria-hidden="true">✨</div>
        <h1>My TODO List</h1>
        <p class="subtitle">Stay organized, one task at a time</p>
      </header>

      <p id="error" class="error" role="alert"></p>

      <form id="add-form">
        <input type="text" id="title" placeholder="What do you need to do?" required />
        <button type="submit"><span class="btn-icon" aria-hidden="true">➕</span>Add task</button>
      </form>

      <ul id="task-list"></ul>
      <p id="empty" class="empty" style="display: none;">
        <span class="empty-icon" aria-hidden="true">📝</span>
        No tasks yet.<br />Add your first one above!
      </p>
    </div>
  </div>

  <script>
    const taskList = document.getElementById("task-list");
    const emptyMsg = document.getElementById("empty");
    const errorEl = document.getElementById("error");
    const addForm = document.getElementById("add-form");
    const titleInput = document.getElementById("title");

    function showError(message) {
      errorEl.textContent = message ? "⚠️ " + message : "";
      errorEl.style.display = message ? "block" : "none";
    }

    async function loadTasks() {
      showError("");
      const response = await fetch("/tasks");
      if (!response.ok) {
        showError("Could not load tasks.");
        return;
      }
      const tasks = await response.json();
      taskList.innerHTML = "";
      emptyMsg.style.display = tasks.length === 0 ? "block" : "none";

      for (const task of tasks) {
        const li = document.createElement("li");
        li.className = "task-item" + (task.completed ? " completed" : "");

        const statusIcon = document.createElement("span");
        statusIcon.className = "task-status";
        statusIcon.setAttribute("aria-hidden", "true");
        statusIcon.textContent = task.completed ? "✅" : "⭕";

        const span = document.createElement("span");
        span.className = "task-title" + (task.completed ? " done" : "");
        span.textContent = task.title;

        const actions = document.createElement("div");
        actions.className = "actions";

        if (!task.completed) {
          const doneBtn = document.createElement("button");
          doneBtn.type = "button";
          doneBtn.className = "secondary";
          doneBtn.innerHTML = '<span class="btn-icon" aria-hidden="true">✓</span>Done';
          doneBtn.onclick = () => completeTask(task.id);
          actions.appendChild(doneBtn);
        }

        const deleteBtn = document.createElement("button");
        deleteBtn.type = "button";
        deleteBtn.className = "danger";
        deleteBtn.innerHTML = '<span class="btn-icon" aria-hidden="true">🗑️</span>Delete';
        deleteBtn.onclick = () => removeTask(task.id);
        actions.appendChild(deleteBtn);

        li.appendChild(statusIcon);
        li.appendChild(span);
        li.appendChild(actions);
        taskList.appendChild(li);
      }
    }

    async function createTask(title) {
      const response = await fetch("/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: title }),
      });
      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        const detail = data.detail;
        const msg = Array.isArray(detail)
          ? detail.map((d) => d.msg).join(", ")
          : detail || "Could not create task.";
        showError(msg);
        return false;
      }
      return true;
    }

    async function completeTask(id) {
      const response = await fetch("/tasks/" + id + "/complete", { method: "PATCH" });
      if (!response.ok) {
        showError("Could not mark task as done.");
        return;
      }
      await loadTasks();
    }

    async function removeTask(id) {
      const response = await fetch("/tasks/" + id, { method: "DELETE" });
      if (!response.ok) {
        showError("Could not delete task.");
        return;
      }
      await loadTasks();
    }

    addForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const title = titleInput.value.trim();
      if (!title) return;

      const ok = await createTask(title);
      if (ok) {
        titleInput.value = "";
        titleInput.focus();
        await loadTasks();
      }
    });

    loadTasks();
  </script>
</body>
</html>
"""


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def todo_homepage() -> HTMLResponse:
    """Serve the TODO list UI."""

    return HTMLResponse(content=TODO_PAGE_HTML)
