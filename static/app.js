/* ═══════════════════════════════════════════════════════════
   Graph Visualizer — Frontend Logic (Method-based workflow)
   ═══════════════════════════════════════════════════════════ */

const SESSION_ID = "default";
const COLORS = ["#03AF7A", "#005AFF", "#FF0000", "#4DC4FF", "#F6AA00", "#FFF100"];

// Preset color palette for easy selection
const COLOR_PRESETS = [
  "#03AF7A", "#005AFF", "#FF0000", "#4DC4FF", "#F6AA00", "#FFF100",
  "#FF4B00", "#9B59B6", "#E91E63", "#00BCD4", "#2ECC71", "#34495E",
  "#1ABC9C", "#E67E22", "#3498DB", "#000000",
];

// ── State ────────────────────────────────────────────────
let state = {
  methods: [],          // [{id, name, color_index, files:[{id, filename, metric, step, value}]}]
  plotData: null,       // {metrics: [{metric, y_label, series:[...]}], methods:[...]}
  activeMetric: null,   // currently selected metric tab
};

// ── Helpers ──────────────────────────────────────────────
function toast(msg, type = "info") {
  const el = document.createElement("div");
  el.className = `toast ${type}`;
  el.textContent = msg;
  document.getElementById("toast-container").appendChild(el);
  setTimeout(() => { el.style.opacity = "0"; setTimeout(() => el.remove(), 300); }, 3000);
}

function parseStepValue(s) {
  if (!s) return null;
  s = s.trim().toUpperCase();
  const mults = { K: 1e3, M: 1e6, B: 1e9 };
  for (const [suffix, mul] of Object.entries(mults)) {
    if (s.endsWith(suffix)) {
      const v = parseFloat(s.slice(0, -1));
      return isNaN(v) ? null : v * mul;
    }
  }
  const v = parseFloat(s);
  return isNaN(v) ? null : v;
}

function getParams() {
  // Build per-method color map
  const methodColors = {};
  state.methods.forEach(m => {
    methodColors[m.id] = m.color || COLORS[m.color_index % COLORS.length];
  });
  return {
    width: parseFloat(document.getElementById("param-width").value) || 10,
    height: parseFloat(document.getElementById("param-height").value) || 7.5,
    min_step: parseStepValue(document.getElementById("param-min-step").value),
    max_step: parseStepValue(document.getElementById("param-max-step").value),
    line_width: parseFloat(document.getElementById("param-line-width").value) || 1.2,
    font_label: parseInt(document.getElementById("param-font-label").value) || 30,
    font_tick: parseInt(document.getElementById("param-font-tick").value) || 25,
    font_legend: parseInt(document.getElementById("param-font-legend").value) || 30,
    dpi: parseInt(document.getElementById("param-dpi").value) || 300,
    show_legend: document.getElementById("param-legend").checked,
    show_grid: document.getElementById("param-grid").checked,
    map_name: document.getElementById("param-map-name").value,
    agent_count: document.getElementById("param-agent-count").value,
    method_colors: methodColors,
  };
}

function togglePanel(id) {
  const el = document.getElementById(id);
  const chevron = document.getElementById(id + "-chevron");
  el.classList.toggle("collapsed");
  if (chevron) chevron.classList.toggle("collapsed");
}

// ── API calls ────────────────────────────────────────────
async function apiAddMethod(name) {
  const res = await fetch("/api/method", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: SESSION_ID, name }),
  });
  return res.json();
}

async function apiDeleteMethod(methodId) {
  await fetch(`/api/method/${methodId}?session_id=${SESSION_ID}`, { method: "DELETE" });
}

async function apiUpdateMethodName(methodId, name) {
  await fetch(`/api/method/${methodId}/name`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: SESSION_ID, name }),
  });
}

async function apiUploadFiles(methodId, fileList) {
  const fd = new FormData();
  fd.append("session_id", SESSION_ID);
  fd.append("method_id", methodId);
  for (const f of fileList) fd.append("files", f);
  const res = await fetch("/api/upload", { method: "POST", body: fd });
  return res.json();
}

async function apiDeleteFile(methodId, fileId) {
  await fetch(`/api/method/${methodId}/file/${fileId}?session_id=${SESSION_ID}`, { method: "DELETE" });
}

async function apiGetPlotData() {
  const res = await fetch(`/api/plot-data?session_id=${SESSION_ID}`);
  return res.json();
}

// ── Add Method ───────────────────────────────────────────
async function addMethod() {
  const name = `手法 ${state.methods.length + 1}`;
  const data = await apiAddMethod(name);
  state.methods.push({
    id: data.method_id,
    name: data.name,
    color_index: data.color_index,
    color: COLORS[data.color_index % COLORS.length],
    files: [],
  });
  renderMethods();
  toast("手法を追加しました", "success");
}

// ── Delete Method ────────────────────────────────────────
async function deleteMethod(methodId) {
  await apiDeleteMethod(methodId);
  state.methods = state.methods.filter(m => m.id !== methodId);
  await refreshPlotData();
  renderMethods();
  renderTabs();
  renderGraph();
  toast("手法を削除しました", "info");
}

// ── Upload Files ─────────────────────────────────────────
async function uploadFiles(methodId, fileList) {
  const result = await apiUploadFiles(methodId, fileList);
  if (result.error) {
    toast(`エラー: ${result.error}`, "error");
    return;
  }

  let successCount = 0;
  for (const r of result.results) {
    if (r.error) {
      toast(`${r.filename}: ${r.error}`, "error");
    } else {
      successCount++;
    }
  }
  if (successCount > 0) {
    toast(`${successCount}個のファイルを追加しました`, "success");
  }

  // Auto-fill map name and agent count from detected values
  if (result.map_name) {
    const mapEl = document.getElementById("param-map-name");
    if (!mapEl.value) mapEl.value = result.map_name;
  }
  if (result.agent_count) {
    const agentEl = document.getElementById("param-agent-count");
    if (!agentEl.value) agentEl.value = result.agent_count;
  }

  await refreshPlotData();
  renderMethods();
  renderTabs();
  renderGraph();
}

// ── Delete File ──────────────────────────────────────────
async function deleteFile(methodId, fileId) {
  await apiDeleteFile(methodId, fileId);
  await refreshPlotData();
  renderMethods();
  renderTabs();
  renderGraph();
}

// ── Refresh plot data from server ────────────────────────
async function refreshPlotData() {
  const data = await apiGetPlotData();
  state.plotData = data;
  // Update local methods with server data
  if (data.methods) {
    // Merge file info from plot data into local state
    const serverMethods = {};
    for (const m of data.methods) {
      serverMethods[m.id] = m;
    }
    // Keep local methods synced
    state.methods = state.methods.filter(m => serverMethods[m.id]);
    for (const m of state.methods) {
      if (serverMethods[m.id]) {
        m.name = serverMethods[m.id].name;
        m.color_index = serverMethods[m.id].color_index;
      }
    }
  }
  // If active metric no longer exists, reset
  if (state.activeMetric && data.metrics) {
    const exists = data.metrics.some(m => m.metric === state.activeMetric);
    if (!exists) state.activeMetric = null;
  }
  // Auto-select first metric if none selected
  if (!state.activeMetric && data.metrics && data.metrics.length > 0) {
    state.activeMetric = data.metrics[0].metric;
  }
}

// ── Render Methods (sidebar) ─────────────────────────────
function renderMethods() {
  const list = document.getElementById("methods-list");
  list.innerHTML = "";

  if (state.methods.length === 0) {
    list.appendChild(createEmptyState());
    return;
  }

  state.methods.forEach((method) => {
    const card = document.createElement("div");
    card.className = "metric-card";
    card.id = `method-card-${method.id}`;

    // Header
    const header = document.createElement("div");
    header.className = "metric-header";

    const dot = document.createElement("input");
    dot.type = "color";
    dot.className = "method-color-picker";
    dot.value = method.color || COLORS[method.color_index % COLORS.length];
    dot.title = "線の色を変更";
    dot.oninput = (e) => {
      method.color = e.target.value;
      renderGraph();
    };

    // Preset color swatches
    const swatchWrap = document.createElement("div");
    swatchWrap.className = "color-preset-row";
    COLOR_PRESETS.forEach(c => {
      const sw = document.createElement("button");
      sw.className = "color-swatch";
      sw.style.background = c;
      sw.title = c;
      sw.onclick = (e) => {
        e.stopPropagation();
        method.color = c;
        dot.value = c;
        renderGraph();
      };
      swatchWrap.appendChild(sw);
    });

    const nameInput = document.createElement("input");
    nameInput.className = "metric-name-input";
    nameInput.value = method.name;
    nameInput.onclick = (e) => e.stopPropagation();
    let nameDebounce;
    nameInput.oninput = (e) => {
      method.name = e.target.value;
      clearTimeout(nameDebounce);
      nameDebounce = setTimeout(async () => {
        await apiUpdateMethodName(method.id, method.name);
        await refreshPlotData();
        renderGraph();
      }, 500);
    };

    const delBtn = document.createElement("button");
    delBtn.className = "metric-delete-btn";
    delBtn.innerHTML = "✕";
    delBtn.title = "手法を削除";
    delBtn.onclick = (e) => { e.stopPropagation(); deleteMethod(method.id); };

    header.appendChild(dot);
    header.appendChild(nameInput);
    header.appendChild(delBtn);
    card.appendChild(header);
    card.appendChild(swatchWrap);

    // Drop zone
    const dropZone = document.createElement("div");
    dropZone.className = "drop-zone";
    dropZone.ondragover = (e) => { e.preventDefault(); dropZone.classList.add("drag-over"); };
    dropZone.ondragleave = () => dropZone.classList.remove("drag-over");
    dropZone.ondrop = (e) => {
      e.preventDefault();
      dropZone.classList.remove("drag-over");
      if (e.dataTransfer.files.length) uploadFiles(method.id, e.dataTransfer.files);
    };

    // Show files grouped by metric (from plotData)
    if (state.plotData && state.plotData.metrics) {
      const methodFiles = [];
      for (const metricGroup of state.plotData.metrics) {
        for (const s of metricGroup.series) {
          if (s.method_id === method.id) {
            methodFiles.push({
              file_id: s.file_id,
              filename: s.filename,
              metric: metricGroup.metric,
              points: s.step.length,
            });
          }
        }
      }

      methodFiles.forEach((f) => {
        const item = document.createElement("div");
        item.className = "file-item";

        const metricTag = document.createElement("span");
        metricTag.className = "file-metric-tag";
        metricTag.textContent = f.metric;

        const fname = document.createElement("span");
        fname.className = "file-name-text";
        fname.textContent = truncateFilename(f.filename, 30);
        fname.title = f.filename;

        const info = document.createElement("span");
        info.className = "file-info";
        info.textContent = `${f.points}pts`;

        const fdel = document.createElement("button");
        fdel.className = "file-delete-btn";
        fdel.innerHTML = "✕";
        fdel.onclick = () => deleteFile(method.id, f.file_id);

        item.appendChild(metricTag);
        item.appendChild(fname);
        item.appendChild(info);
        item.appendChild(fdel);
        dropZone.appendChild(item);
      });
    }

    // Upload label
    const uploadLabel = document.createElement("label");
    uploadLabel.className = "drop-zone-label";
    uploadLabel.innerHTML = `<span>📁</span> CSVファイルをドラッグ＆ドロップ`;
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = ".csv";
    fileInput.multiple = true;
    fileInput.onchange = (e) => {
      if (e.target.files.length) uploadFiles(method.id, e.target.files);
    };
    uploadLabel.appendChild(fileInput);
    dropZone.appendChild(uploadLabel);

    card.appendChild(dropZone);
    list.appendChild(card);
  });
}

function truncateFilename(name, maxLen) {
  if (name.length <= maxLen) return name;
  const ext = name.slice(name.lastIndexOf("."));
  return name.slice(0, maxLen - ext.length - 3) + "..." + ext;
}

function createEmptyState() {
  const div = document.createElement("div");
  div.className = "empty-state";
  div.innerHTML = '<p>「＋ 手法追加」ボタンで<br>手法を追加してください<br><small>例: 従来手法, 提案手法, 関連研究</small></p>';
  return div;
}

// ── Render Tabs (one per detected metric) ────────────────
function renderTabs() {
  const bar = document.getElementById("tab-bar");
  bar.innerHTML = "";

  if (!state.plotData || !state.plotData.metrics || state.plotData.metrics.length === 0) {
    return;
  }

  state.plotData.metrics.forEach(m => {
    const tab = document.createElement("button");
    tab.className = `tab-btn ${m.metric === state.activeMetric ? "active" : ""}`;
    tab.textContent = m.y_label || m.metric;
    tab.onclick = () => {
      state.activeMetric = m.metric;
      renderTabs();
      renderGraph();
    };
    bar.appendChild(tab);
  });
}

// ── Render Graph (Matplotlib Preview) ─────────────────────
let currentPreviewUrl = null;

async function renderGraph() {
  const wrapper = document.getElementById("preview-wrapper");
  const imgData = document.getElementById("matplotlib-preview");
  const placeholder = document.getElementById("graph-placeholder");
  const loading = document.getElementById("loading-overlay");
  const params = getParams();

  if (!state.plotData || !state.plotData.metrics || state.plotData.metrics.length === 0) {
    wrapper.style.display = "none";
    placeholder.style.display = "flex";
    return;
  }

  const metricData = state.plotData.metrics.find(m => m.metric === state.activeMetric);
  if (!metricData || !metricData.series || metricData.series.length === 0) {
    wrapper.style.display = "none";
    placeholder.style.display = "flex";
    return;
  }

  placeholder.style.display = "none";
  wrapper.style.display = "none";
  loading.style.display = "flex";

  params.y_label = metricData.y_label || "Value";
  params.x_label = "Training steps";

  // Populate stats
  const statsContainer = document.getElementById("stats-container");
  const statsContent = document.getElementById("stats-content");
  if (statsContainer && statsContent) {
    if (metricData.stats && metricData.stats.length > 0) {
      statsContainer.style.display = "block";
      statsContent.innerHTML = "";
      metricData.stats.forEach(st => {
        const card = document.createElement("div");
        card.style.flex = "1 1 200px";
        card.style.background = "var(--bg-body, #f9fafb)";
        card.style.border = "1px solid var(--border-color, #e5e7eb)";
        card.style.borderRadius = "8px";
        card.style.padding = "10px 14px";

        const dot = document.createElement("span");
        dot.style.display = "inline-block";
        dot.style.width = "12px";
        dot.style.height = "12px";
        dot.style.borderRadius = "50%";
        dot.style.background = params.method_colors[st.method_id] || COLORS[st.color_index % COLORS.length];
        dot.style.marginRight = "8px";

        const title = document.createElement("div");
        title.style.display = "flex";
        title.style.alignItems = "center";
        title.style.fontWeight = "600";
        title.style.fontSize = "13px";
        title.style.color = "var(--text-main, #111827)";
        title.style.marginBottom = "4px";
        title.appendChild(dot);
        title.appendChild(document.createTextNode(st.method_name));
        if (st.n_runs > 1) {
          const span = document.createElement("span");
          span.style.fontSize = "11px";
          span.style.color = "var(--text-muted, #6b7280)";
          span.style.marginLeft = "6px";
          span.textContent = `(${st.n_runs} runs)`;
          title.appendChild(span);
        }

        const val = document.createElement("div");
        val.style.fontSize = "16px";
        val.style.fontFamily = "monospace";
        val.style.color = "var(--text-main, #374151)";
        val.textContent = `${st.mean.toFixed(4)} ± ${st.std.toFixed(4)}`;

        card.appendChild(title);
        card.appendChild(val);
        statsContent.appendChild(card);
      });
    } else {
      statsContainer.style.display = "none";
    }
  }

  try {
    const res = await fetch("/api/export", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: SESSION_ID,
        metric: state.activeMetric,
        format: "png",
        params: params,
      }),
    });

    if (!res.ok) {
      const err = await res.json();
      toast(`プレビュー生成エラー: ${err.error}`, "error");
      loading.style.display = "none";
      return;
    }

    const blob = await res.blob();
    if (currentPreviewUrl) {
      URL.revokeObjectURL(currentPreviewUrl);
    }
    currentPreviewUrl = URL.createObjectURL(blob);
    imgData.src = currentPreviewUrl;

    loading.style.display = "none";
    wrapper.style.display = "flex";
  } catch (e) {
    toast(`プレビュー生成失敗: ${e.message}`, "error");
    loading.style.display = "none";
  }
}

// ── Export ────────────────────────────────────────────────
async function exportCurrent(format) {
  if (!state.activeMetric) {
    toast("グラフが表示されていません", "error");
    return;
  }

  const params = getParams();
  const metricData = state.plotData?.metrics?.find(m => m.metric === state.activeMetric);
  if (metricData) {
    params.y_label = metricData.y_label || "Value";
  }
  params.x_label = "Training steps";

  toast(`${format.toUpperCase()} エクスポート中...`, "info");

  try {
    const res = await fetch("/api/export", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: SESSION_ID,
        metric: state.activeMetric,
        format: format,
        params: params,
      }),
    });

    if (!res.ok) {
      const err = await res.json();
      toast(`エラー: ${err.error}`, "error");
      return;
    }

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    // Build filename: {map}_{agents}agent_{metric}_{figsize}.{fmt}
    const parts = [];
    if (params.map_name) parts.push(params.map_name);
    if (params.agent_count) parts.push(`${params.agent_count}agent`);
    parts.push(state.activeMetric);
    parts.push(`${Math.round(params.width)}-${Math.round(params.height)}`);
    a.download = parts.join("_") + `.${format}`;
    a.click();
    URL.revokeObjectURL(url);
    toast(`${format.toUpperCase()} をダウンロードしました`, "success");
  } catch (e) {
    toast(`エクスポート失敗: ${e.message}`, "error");
  }
}

// ── Export All (ZIP) ─────────────────────────────────────
async function exportAll(format) {
  if (!state.plotData || !state.plotData.metrics || state.plotData.metrics.length === 0) {
    toast("エクスポートするグラフがありません", "error");
    return;
  }

  const params = getParams();
  toast(`全メトリクス ${format.toUpperCase()} 一括エクスポート中...`, "info");

  try {
    const res = await fetch("/api/export-all", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: SESSION_ID,
        format: format,
        params: params,
      }),
    });

    if (!res.ok) {
      const err = await res.json();
      toast(`エラー: ${err.error}`, "error");
      return;
    }

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `graphs_${format}.zip`;
    a.click();
    URL.revokeObjectURL(url);
    toast(`${state.plotData.metrics.length}件のグラフをZIPでダウンロードしました`, "success");
  } catch (e) {
    toast(`一括エクスポート失敗: ${e.message}`, "error");
  }
}

// ── Auto-update graph on param change ────────────────────
document.querySelectorAll("#params-content input").forEach(el => {
  const evts = el.type === "checkbox" ? ["change"] : ["change", "input"];
  evts.forEach(evt => el.addEventListener(evt, () => renderGraph()));
});

// ── Initialize ───────────────────────────────────────────
renderMethods();
renderTabs();
