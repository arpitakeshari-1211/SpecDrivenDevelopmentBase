"""Simple HTML frontend for the TODO app."""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["ui"])

# Plain HTML + CSS + JavaScript; calls the JSON API at /tasks.
TODO_PAGE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>TODO App</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
      min-height: 100vh;
      padding: clamp(1rem, 4vw, 2.5rem);
      color: #f8fafc;
      background: linear-gradient(135deg, #0f172a, #4338ca 50%, #a855f7);
      background-attachment: fixed;
    }

    .card {
      max-width: 520px;
      margin: 0 auto;
      padding: clamp(1.25rem, 4vw, 2rem);
      border-radius: 20px;
      background: rgba(255, 255, 255, 0.12);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.25);
      box-shadow: 0 12px 40px rgba(15, 23, 42, 0.35);
    }

    h1 {
      text-align: center;
      font-size: clamp(1.4rem, 4vw, 1.75rem);
      margin-bottom: 0.25rem;
    }

    .subtitle {
      text-align: center;
      color: rgba(248, 250, 252, 0.75);
      font-size: 0.9rem;
      margin-bottom: 1.5rem;
    }

    .error {
      display: none;
      margin-bottom: 1rem;
      padding: 0.75rem 1rem;
      border-radius: 12px;
      background: rgba(239, 68, 68, 0.25);
      border: 1px solid rgba(252, 165, 165, 0.4);
      color: #fecaca;
      font-size: 0.9rem;
    }

    form {
      display: flex;
      flex-wrap: wrap;
      gap: 0.6rem;
      margin-bottom: 1.25rem;
    }

    input[type="text"] {
      flex: 1 1 160px;
      min-width: 0;
      padding: 0.8rem 1rem;
      border-radius: 14px;
      border: 1px solid rgba(255, 255, 255, 0.3);
      background: rgba(255, 255, 255, 0.1);
      color: #fff;
      font-size: 1rem;
      transition: box-shadow 0.2s ease, border-color 0.2s ease;
    }

    input::placeholder { color: rgba(255, 255, 255, 0.5); }

    input:focus {
      outline: none;
      border-color: #c4b5fd;
      box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.35);
    }

    button {
      padding: 0.8rem 1.1rem;
      border: none;
      border-radius: 14px;
      font-weight: 600;
      cursor: pointer;
      color: #fff;
      background: linear-gradient(135deg, #6366f1, #8b5cf6);
      box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    button:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
    }

    button.secondary {
      background: rgba(255, 255, 255, 0.15);
      box-shadow: none;
      border: 1px solid rgba(255, 255, 255, 0.25);
    }

    button.danger {
      background: rgba(239, 68, 68, 0.3);
      border: 1px solid rgba(252, 165, 165, 0.35);
      box-shadow: none;
    }

    ul { list-style: none; display: flex; flex-direction: column; gap: 0.65rem; }

    li {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.6rem;
      padding: 0.9rem 1rem;
      border-radius: 14px;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.15);
      transition: transform 0.2s ease, opacity 0.25s ease;
    }

    li:hover { transform: translateY(-1px); }

    li.done-item {
      opacity: 0.55;
    }

    li.done-item:hover { transform: none; }

    .task-title {
      flex: 1 1 120px;
      word-break: break-word;
    }

    .task-title.completed {
      text-decoration: line-through;
      color: rgba(248, 250, 252, 0.55);
    }

    .actions {
      display: flex;
      gap: 0.35rem;
      margin-left: auto;
    }

    .actions button { padding: 0.45rem 0.75rem; font-size: 0.85rem; }

    .empty {
      text-align: center;
      padding: 1.5rem;
      color: rgba(248, 250, 252, 0.7);
      border: 1px dashed rgba(255, 255, 255, 0.25);
      border-radius: 14px;
    }

    @media (max-width: 480px) {
      form { flex-direction: column; }
      form button { width: 100%; }
      .actions { width: 100%; justify-content: flex-end; margin-left: 0; }
    }
  </style>
</head>
<body>
  <main class="card">
    <h1>✨ TODO App</h1>
    <p class="subtitle">Spec-driven FastAPI demo</p>

    <p id="error" class="error" role="alert"></p>

    <form id="add-form">
      <input id="title" type="text" placeholder="New task title…" required />
      <button type="submit">➕ Add</button>
    </form>

    <ul id="task-list"></ul>
    <p id="empty" class="empty" style="display: none;">📝 No tasks yet. Add one above!</p>
  </main>

  <script>
    const taskList = document.getElementById("task-list");
    const emptyMsg = document.getElementById("empty");
    const errorEl = document.getElementById("error");
    const addForm = document.getElementById("add-form");
    const titleInput = document.getElementById("title");

    function showError(msg) {
      errorEl.textContent = msg ? "⚠️ " + msg : "";
      errorEl.style.display = msg ? "block" : "none";
    }

    async function loadTasks() {
      showError("");
      const res = await fetch("/tasks");
      if (!res.ok) {
        showError("Could not load tasks.");
        return;
      }
      const tasks = await res.json();
      taskList.innerHTML = "";
      emptyMsg.style.display = tasks.length ? "none" : "block";

      for (const task of tasks) {
        const li = document.createElement("li");
        if (task.completed) li.className = "done-item";

        const icon = document.createElement("span");
        icon.textContent = task.completed ? "✅" : "⭕";
        icon.setAttribute("aria-hidden", "true");

        const title = document.createElement("span");
        title.className = "task-title" + (task.completed ? " completed" : "");
        title.textContent = task.title;

        const actions = document.createElement("div");
        actions.className = "actions";

        if (!task.completed) {
          const doneBtn = document.createElement("button");
          doneBtn.type = "button";
          doneBtn.className = "secondary";
          doneBtn.textContent = "✓ Done";
          doneBtn.onclick = () => completeTask(task.id);
          actions.appendChild(doneBtn);
        }

        const delBtn = document.createElement("button");
        delBtn.type = "button";
        delBtn.className = "danger";
        delBtn.textContent = "🗑 Delete";
        delBtn.onclick = () => deleteTask(task.id);
        actions.appendChild(delBtn);

        li.append(icon, title, actions);
        taskList.appendChild(li);
      }
    }

    async function createTask(title) {
      const res = await fetch("/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title }),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        const d = data.detail;
        showError(Array.isArray(d) ? d.map((x) => x.msg).join(", ") : d || "Could not add task.");
        return false;
      }
      return true;
    }

    async function completeTask(id) {
      const res = await fetch("/tasks/" + id + "/complete", { method: "PATCH" });
      if (!res.ok) {
        showError("Could not complete task.");
        return;
      }
      await loadTasks();
    }

    async function deleteTask(id) {
      const res = await fetch("/tasks/" + id, { method: "DELETE" });
      if (!res.ok) {
        showError("Could not delete task.");
        return;
      }
      await loadTasks();
    }

    addForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const title = titleInput.value.trim();
      if (!title) return;
      if (await createTask(title)) {
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
    """Homepage with the TODO UI."""

    return HTMLResponse(content=TODO_PAGE_HTML)
