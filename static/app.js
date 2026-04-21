const form = document.getElementById("generate-form");
const taskSection = document.getElementById("task-section");
const taskIdEl = document.getElementById("task-id");
const videoIdEl = document.getElementById("video-id");
const statusEl = document.getElementById("status");
const progressTextEl = document.getElementById("progress-text");
const progressBarEl = document.getElementById("progress-bar");
const errorEl = document.getElementById("error");
const downloadLinkEl = document.getElementById("download-link");

let pollTimer = null;

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const prompt = document.getElementById("prompt").value.trim();
  if (!prompt) {
    return;
  }

  clearPoll();
  resetUi();

  const response = await fetch("/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt }),
  });

  const payload = await response.json();
  if (!response.ok) {
    errorEl.textContent = payload.error || "Не удалось создать задачу";
    return;
  }

  taskSection.classList.remove("hidden");
  taskIdEl.textContent = payload.task_id;
  statusEl.textContent = "queued";
  progressTextEl.textContent = "0%";

  pollTimer = setInterval(() => pollStatus(payload.task_id), 1500);
  await pollStatus(payload.task_id);
});

async function pollStatus(taskId) {
  const response = await fetch(`/status/${taskId}`);
  if (!response.ok) {
    errorEl.textContent = "Не удалось получить статус задачи";
    clearPoll();
    return;
  }

  const task = await response.json();
  statusEl.textContent = task.status;
  videoIdEl.textContent = task.video_id || "-";

  const progress = Number(task.progress || 0);
  progressTextEl.textContent = `${Math.round(progress)}%`;
  progressBarEl.style.width = `${Math.max(0, Math.min(100, progress))}%`;

  if (task.error_message) {
    errorEl.textContent = task.error_message;
  }

  if (task.status === "completed") {
    downloadLinkEl.href = `/download/${taskId}`;
    downloadLinkEl.classList.remove("hidden");
    clearPoll();
  }

  if (task.status === "failed" || task.status === "error") {
    clearPoll();
  }
}

function clearPoll() {
  if (pollTimer !== null) {
    clearInterval(pollTimer);
    pollTimer = null;
  }
}

function resetUi() {
  taskSection.classList.remove("hidden");
  taskIdEl.textContent = "-";
  videoIdEl.textContent = "-";
  statusEl.textContent = "queued";
  progressTextEl.textContent = "0%";
  progressBarEl.style.width = "0%";
  errorEl.textContent = "";
  downloadLinkEl.classList.add("hidden");
  downloadLinkEl.href = "#";
}
