const capabilitySummary = document.querySelector("#capabilitySummary");
const toolList = document.querySelector("#toolList");
const jobForm = document.querySelector("#jobForm");
const currentJob = document.querySelector("#currentJob");
const jobList = document.querySelector("#jobList");
const refreshCapabilities = document.querySelector("#refreshCapabilities");

let activeJobId = null;
let pollTimer = null;

async function loadCapabilities() {
  const response = await fetch("/api/capabilities");
  const data = await response.json();
  capabilitySummary.textContent = `当前能力等级：${data.level}`;
  toolList.innerHTML = data.tools
    .map((tool) => {
      const cls = tool.available ? "ok" : "missing";
      const state = tool.available ? "可用" : "缺少";
      return `<div class="tool"><strong>${tool.name}</strong> <span class="${cls}">${state}</span><br><small>${tool.purpose}｜${tool.detail}</small></div>`;
    })
    .join("");
}

function renderJob(job) {
  const download = job.status === "completed"
    ? `<p><a href="/api/jobs/${job.job_id}/download">下载 MP4</a></p>`
    : "";
  const progress = (job.progress || []).map((item) => `<li>${item}</li>`).join("");
  const error = job.error ? `<p class="failed">${job.error}</p>` : "";
  return `<div class="job">
    <strong>${job.output_name || job.job_id}</strong>
    <p>状态：${job.status}</p>
    ${error}
    <ul>${progress}</ul>
    ${download}
  </div>`;
}

async function loadJobs() {
  const response = await fetch("/api/jobs");
  const jobs = await response.json();
  jobList.innerHTML = jobs.length ? jobs.map(renderJob).join("") : '<div class="empty">暂无历史任务。</div>';
}

async function pollJob(jobId) {
  const response = await fetch(`/api/jobs/${jobId}`);
  const job = await response.json();
  currentJob.innerHTML = renderJob(job);
  await loadJobs();
  if (["completed", "failed", "needs_script"].includes(job.status)) {
    clearInterval(pollTimer);
    pollTimer = null;
  }
}

jobForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(jobForm);
  currentJob.textContent = "正在上传并创建任务...";
  const response = await fetch("/api/jobs", { method: "POST", body: formData });
  if (!response.ok) {
    const error = await response.json();
    currentJob.innerHTML = `<p class="failed">${error.detail || "创建任务失败"}</p>`;
    return;
  }
  const job = await response.json();
  activeJobId = job.job_id;
  currentJob.innerHTML = renderJob(job);
  if (pollTimer) {
    clearInterval(pollTimer);
  }
  pollTimer = setInterval(() => pollJob(activeJobId), 1600);
});

refreshCapabilities.addEventListener("click", loadCapabilities);

loadCapabilities();
loadJobs();
