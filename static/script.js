const API = "/tasks";

const taskList  = document.getElementById("task-list");
const emptyMsg  = document.getElementById("empty-msg");
const errorMsg  = document.getElementById("error-msg");
const addForm   = document.getElementById("add-form");
const newTitle  = document.getElementById("new-title");

function showError(msg) {
  errorMsg.textContent = msg;
  errorMsg.classList.remove("hidden");
  setTimeout(() => errorMsg.classList.add("hidden"), 4000);
}

function renderTasks(tasks) {
  taskList.innerHTML = "";
  emptyMsg.classList.toggle("hidden", tasks.length > 0);

  tasks.forEach(task => {
    const li = document.createElement("li");
    li.className = "task-item" + (task.completed ? " completed" : "");
    li.dataset.id = task._id;

    li.innerHTML = `
      <label class="checkbox-label">
        <input type="checkbox" class="toggle-cb" ${task.completed ? "checked" : ""} />
        <span class="title-text">${escapeHtml(task.title)}</span>
      </label>
      <div class="actions">
        <button class="btn-edit" title="Edit">&#9998;</button>
        <button class="btn-delete" title="Delete">&#10005;</button>
      </div>
    `;

    li.querySelector(".toggle-cb").addEventListener("change", () => toggleTask(task._id, !task.completed));
    li.querySelector(".btn-delete").addEventListener("click", () => deleteTask(task._id));
    li.querySelector(".btn-edit").onclick = () => startEdit(li, task, task._id);

    taskList.appendChild(li);
  });
}

function escapeHtml(str) {
  return str.replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[c]));
}

async function loadTasks() {
  try {
    const res  = await fetch(API);
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to load tasks");
    // שים לב: אם השרת מחזיר רשימה ישירות, השתמש ב-data במקום data.data
    renderTasks(Array.isArray(data) ? data : data.data);
  } catch (e) {
    showError(e.message);
  }
}

async function createTask(title) {
  const res  = await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Failed to create task");
  return data;
}

async function toggleTask(id, completed) {
  try {
    const res  = await fetch(`${API}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ completed }),
    });
    if (!res.ok) throw new Error("Failed to update task");
    loadTasks();
  } catch (e) {
    showError(e.message);
  }
}

async function deleteTask(id) {
  try {
    const res  = await fetch(`${API}/${id}`, { method: "DELETE" });
    if (!res.ok) throw new Error("Failed to delete task");
    loadTasks();
  } catch (e) {
    showError(e.message);
  }
}

async function saveEdit(id, newTitleValue, li) {
  try {
    const res  = await fetch(`${API}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: newTitleValue }),
    });
    if (!res.ok) throw new Error("Failed to update task");
    loadTasks();
  } catch (e) {
    showError(e.message);
  }
}

function startEdit(li, task, id) {
  const label = li.querySelector(".checkbox-label");
  const titleSpan = li.querySelector(".title-text");
  const editBtn = li.querySelector(".btn-edit");

  const input = document.createElement("input");
  input.type = "text";
  input.className = "edit-input";
  input.value = task.title;

  label.replaceChild(input, titleSpan);
  editBtn.textContent = "Save";
  input.focus();

  const finish = () => {
    const val = input.value.trim();
    if (val && val !== task.title) {
      saveEdit(id, val, li);
    } else {
      loadTasks();
    }
  };

  editBtn.onclick = finish;
  input.addEventListener("keydown", e => {
    if (e.key === "Enter") finish();
    if (e.key === "Escape") loadTasks();
  });
}

addForm.addEventListener("submit", async e => {
  e.preventDefault();
  const title = newTitle.value.trim();
  if (!title) return;
  try {
    await createTask(title);
    newTitle.value = "";
    loadTasks();
  } catch (e) {
    showError(e.message);
  }
});

loadTasks();