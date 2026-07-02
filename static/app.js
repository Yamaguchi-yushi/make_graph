
const i18n = {
  ja: {
    "title": "Graph Visualizer — CSV可視化ツール",
    "subtitle": "CSVファイルからインタラクティブなグラフを作成",
    "settings": "⚙️ グラフ設定",
    "map_name": "マップ名",
    "agent_count": "エージェント数",
    "auto_detect": "自動検出",
    "memo": "📝 メモ（ファイル名に反映）",
    "memo_placeholder": "例: 比較実験1",
    "width": "幅",
    "height": "高さ",
    "step_min": "ステップ最小",
    "step_max": "ステップ最大",
    "ex_step_min": "例: 0, 1M",
    "ex_step_max": "例: 8M",
    "axis_label": "軸ラベル",
    "axis_tick": "軸の数値",
    "legend_size": "凡例",
    "legend_position": "凡例の位置",
    "legend_reset": "自動に戻す",
    "legend_auto": "自動",
    "show_legend": "凡例を表示",
    "show_grid": "グリッド",
    "show_range": "範囲表示",
    "methods": "🔬 手法",
    "add_method": "＋ 手法追加",
    "empty_methods": "「＋ 手法追加」ボタンで<br>手法を追加してください<br><small>例: 従来手法, 提案手法, 関連研究</small>",
    "export_all_png": "📦 PNG全保存",
    "export_all_pdf": "📦 PDF全保存",
    "export_all_eps": "📦 EPS全保存",
    "graph_placeholder": "指標を追加してCSVファイルをアップロードすると<br>ここにグラフが表示されます",
    "generating": "画像を生成中...",
    "final_perf": "📊 最終パフォーマンス (最後10%の平均 ± 標準偏差)",
    "toggle_lang": "🌐 Language",
    "drop_csv": "<span>📁</span> CSVファイルをドラッグ＆ドロップ",
    "method_added": "手法を追加しました",
    "method_deleted": "手法を削除しました",
    "files_added": "個のファイルを追加しました",
    "method_prefix": "手法 ",
    "error_prefix": "エラー: ",
    "attention_prefix": "⚠️ 注意: ",
    "no_graph": "グラフが表示されていません",
    "exporting": "エクスポート中...",
    "downloaded": "をダウンロードしました",
    "export_failed": "エクスポート失敗: ",
    "no_export": "エクスポートするグラフがありません",
    "all_metrics": "全メトリクス ",
    "batch_exporting": " 一括エクスポート中...",
    "graphs_zip_downloaded": "件のグラフをZIPでダウンロードしました",
    "batch_export_failed": "一括エクスポート失敗: ",
    "export_csv_zip": "📁 CSV整理",
    "export_single": "📥 1枚保存",
    "export_all": "📦 全て保存",
    "export_legend": "🏷️ 凡例PDF出力",
    "mode_graph": "📊 グラフ作成",
    "mode_legend": "🏷️ 凡例出力",
    "legend_rows": "行数",
    "legend_rows_auto": "自動",
    "legend_rows_1": "1行",
    "legend_rows_2": "2行",
    "legend_rows_manual": "列数指定",
    "legend_ncol": "列数",
    "legend_orient": "向き",
    "legend_orient_h": "横",
    "legend_orient_v": "縦",
    "legend_lw": "線の太さ",
    "legend_font": "文字",
    "legend_frame": "枠",
    "legend_transparent": "背景透過",
    "category": "🏷️ 種別（任意・ファイル名に反映）",
    "category_placeholder": "任意 例: ablation",
    "csv_exporting": "CSVファイルを整理してエクスポート中...",
    "csv_zip_downloaded": "CSVファイルをフォルダ整理してダウンロードしました",
    "csv_export_failed": "CSVエクスポート失敗: ",
    "clear_all_csvs": "🗑️ 全CSV削除",
    "confirm_clear_csvs": "全ての手法のCSVファイルを一括削除しますか？",
    "csvs_cleared": "全CSVファイルを削除しました",
    "load_folder": "📁 フォルダ読込",
    "smoothing": "スムージング"
  },
  en: {
    "title": "Graph Visualizer",
    "subtitle": "Create interactive graphs from CSV files",
    "settings": "⚙️ Graph Settings",
    "map_name": "Map Name",
    "agent_count": "Agents",
    "auto_detect": "Auto-detect",
    "memo": "📝 Memo (reflected in filenames)",
    "memo_placeholder": "e.g., Experiment 1",
    "width": "Width",
    "height": "Height",
    "step_min": "Min Step",
    "step_max": "Max Step",
    "ex_step_min": "e.g., 0, 1M",
    "ex_step_max": "e.g., 8M",
    "axis_label": "Axis Label Size",
    "axis_tick": "Tick Size",
    "legend_size": "Legend Size",
    "legend_position": "Legend Position",
    "legend_reset": "Reset to Auto",
    "legend_auto": "Auto",
    "show_legend": "Show Legend",
    "show_grid": "Show Grid",
    "show_range": "Show Range",
    "methods": "🔬 Methods",
    "add_method": "＋ Add Method",
    "empty_methods": "Click \"＋ Add Method\" to add a method<br><small>e.g., Baseline, Proposed, Related Work</small>",
    "export_all_png": "📦 Export All PNG",
    "export_all_pdf": "📦 Export All PDF",
    "export_all_eps": "📦 Export All EPS",
    "graph_placeholder": "Add a method and upload CSV files<br>to display the graph here",
    "generating": "Generating image...",
    "final_perf": "📊 Final Performance (Last 10% steps Mean ± STD)",
    "toggle_lang": "🌐 Language",
    "drop_csv": "<span>📁</span> Drag & Drop CSV files",
    "method_added": "Method added",
    "method_deleted": "Method deleted",
    "files_added": " files added",
    "method_prefix": "Method ",
    "error_prefix": "Error: ",
    "attention_prefix": "⚠️ Note: ",
    "no_graph": "No graph displayed",
    "exporting": "Exporting...",
    "downloaded": " downloaded",
    "export_failed": "Export failed: ",
    "no_export": "No graphs to export",
    "all_metrics": "All metrics ",
    "batch_exporting": " batch exporting...",
    "graphs_zip_downloaded": " graphs downloaded as ZIP",
    "batch_export_failed": "Batch export failed: ",
    "export_csv_zip": "📁 Organize CSV",
    "export_single": "📥 Save one",
    "export_all": "📦 Save all",
    "export_legend": "🏷️ Export Legend PDF",
    "mode_graph": "📊 Graph",
    "mode_legend": "🏷️ Legend",
    "legend_rows": "Rows",
    "legend_rows_auto": "Auto",
    "legend_rows_1": "1 row",
    "legend_rows_2": "2 rows",
    "legend_rows_manual": "Set columns",
    "legend_ncol": "Cols",
    "legend_orient": "Orient.",
    "legend_orient_h": "Horizontal",
    "legend_orient_v": "Vertical",
    "legend_lw": "Line width",
    "legend_font": "Font",
    "legend_frame": "Frame",
    "legend_transparent": "Transparent",
    "category": "🏷️ Tag (optional, in filename)",
    "category_placeholder": "optional e.g. ablation",
    "csv_exporting": "Organizing and exporting CSV files...",
    "csv_zip_downloaded": "CSV files downloaded in organized folders",
    "csv_export_failed": "CSV export failed: ",
    "clear_all_csvs": "🗑️ Clear All CSVs",
    "confirm_clear_csvs": "Are you sure you want to remove all CSV files from all methods?",
    "csvs_cleared": "All CSV files cleared",
    "smoothing": "smoothing",
    "load_folder": "📁 Load Folder"
  },
  fr: {
    "title": "Graph Visualizer — Outil de visualisation CSV",
    "subtitle": "Créer des graphiques interactifs à partir de fichiers CSV",
    "settings": "⚙️ Paramètres du graphique",
    "map_name": "Nom de la carte",
    "agent_count": "Nb d'agents",
    "auto_detect": "Auto-détection",
    "memo": "📝 Mémo (inclus dans les noms de fichiers)",
    "memo_placeholder": "ex. Expérience 1",
    "width": "Largeur",
    "height": "Hauteur",
    "step_min": "Pas min",
    "step_max": "Pas max",
    "ex_step_min": "ex. 0, 1M",
    "ex_step_max": "ex. 8M",
    "axis_label": "Taille des labels",
    "axis_tick": "Taille des graduations",
    "legend_size": "Taille de la légende",
    "legend_position": "Position de la légende",
    "legend_reset": "Réinitialiser",
    "legend_auto": "Auto",
    "show_legend": "Afficher la légende",
    "show_grid": "Afficher la grille",
    "show_range": "Afficher la plage",
    "methods": "🔬 Méthodes",
    "add_method": "＋ Ajouter une méthode",
    "empty_methods": "Cliquez sur \"Ajouter une méthode\" pour commencer<br><small>ex. Méthode de base, Méthode proposée, Travaux connexes</small>",
    "export_all_png": "📦 Tout en PNG",
    "export_all_pdf": "📦 Tout en PDF",
    "export_all_eps": "📦 Tout en EPS",
    "graph_placeholder": "Ajoutez une méthode et téléversez des fichiers CSV<br>pour afficher le graphique ici",
    "generating": "Génération de l'image...",
    "final_perf": "📊 Performance finale (Moyenne ± Écart-type des derniers 10%)",
    "toggle_lang": "🌐 Language",
    "drop_csv": "<span>📁</span> Glisser-déposer des fichiers CSV",
    "method_added": "Méthode ajoutée",
    "method_deleted": "Méthode supprimée",
    "files_added": " fichiers ajoutés",
    "method_prefix": "Méthode ",
    "error_prefix": "Erreur : ",
    "attention_prefix": "⚠️ Attention : ",
    "no_graph": "Aucun graphique affiché",
    "exporting": "Exportation en cours...",
    "downloaded": " téléchargé",
    "export_failed": "Échec de l'exportation : ",
    "no_export": "Aucun graphique à exporter",
    "all_metrics": "Toutes les métriques ",
    "batch_exporting": " exportation groupée en cours...",
    "graphs_zip_downloaded": " graphiques téléchargés en ZIP",
    "batch_export_failed": "Échec de l'exportation groupée : ",
    "export_csv_zip": "📁 Organiser CSV",
    "export_single": "📥 Enregistrer 1",
    "export_all": "📦 Tout enregistrer",
    "export_legend": "🏷️ Exporter la légende PDF",
    "mode_graph": "📊 Graphique",
    "mode_legend": "🏷️ Légende",
    "legend_rows": "Lignes",
    "legend_rows_auto": "Auto",
    "legend_rows_1": "1 ligne",
    "legend_rows_2": "2 lignes",
    "legend_rows_manual": "Colonnes",
    "legend_ncol": "Col.",
    "legend_orient": "Orient.",
    "legend_orient_h": "Horizontal",
    "legend_orient_v": "Vertical",
    "legend_lw": "Épaisseur",
    "legend_font": "Police",
    "legend_frame": "Cadre",
    "legend_transparent": "Transparent",
    "category": "🏷️ Type (optionnel, dans le nom)",
    "category_placeholder": "optionnel ex: ablation",
    "csv_exporting": "Organisation et exportation des fichiers CSV...",
    "csv_zip_downloaded": "Fichiers CSV téléchargés dans des dossiers organisés",
    "csv_export_failed": "Échec de l'exportation CSV : ",
    "clear_all_csvs": "🗑️ Effacer tous les CSV",
    "confirm_clear_csvs": "Voulez-vous vraiment supprimer tous les fichiers CSV de toutes les méthodes ?",
    "csvs_cleared": "Tous les fichiers CSV ont été supprimés",
    "smoothing": "lissage",
    "load_folder": "📁 Charger Dossier"
  }
};
let currentLang = localStorage.getItem("lang") || "ja";

function t(key) {
  return i18n[currentLang][key] || key;
}

const LANG_ORDER = ["ja", "en", "fr"];

function toggleLangMenu() {
  const menu = document.getElementById("lang-menu");
  menu.classList.toggle("show");
}

function setLanguage(lang) {
  currentLang = lang;
  localStorage.setItem("lang", currentLang);
  document.getElementById("lang-menu").classList.remove("show");
  applyTranslations();
  renderMethods();
}

// Close dropdown when clicking outside
document.addEventListener("click", (e) => {
  const dropdown = document.getElementById("lang-dropdown");
  if (dropdown && !dropdown.contains(e.target)) {
    document.getElementById("lang-menu").classList.remove("show");
  }
  // Export dropdowns: close when clicking outside either one
  const single = document.getElementById("export-single-dropdown");
  const all = document.getElementById("export-all-dropdown");
  if ((!single || !single.contains(e.target)) &&
      (!all || !all.contains(e.target))) {
    closeExportMenus();
  }
});

function closeExportMenus() {
  document.getElementById("export-single-menu")?.classList.remove("show");
  document.getElementById("export-all-menu")?.classList.remove("show");
}

function toggleExportMenu(which) {
  const target = document.getElementById(
    which === "single" ? "export-single-menu" : "export-all-menu");
  const other = document.getElementById(
    which === "single" ? "export-all-menu" : "export-single-menu");
  other?.classList.remove("show");
  target?.classList.toggle("show");
}

function applyTranslations() {
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (key) {
      if (el.tagName === "INPUT" && el.hasAttribute("placeholder")) {
        el.placeholder = t(key);
      } else {
        el.innerHTML = t(key);
      }
    }
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (key) el.placeholder = t(key);
  });
  document.title = t("title");
}
// Init translations on load
document.addEventListener("DOMContentLoaded", applyTranslations);

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
  expandedMethods: new Set(),  // track which method cards are expanded
  legendSettings: {},   // metric -> {auto: true, x: 1.0, y: 1.0}
  mode: "graph",        // "graph" | "legend"
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
    width: parseFloat(document.getElementById("param-width").value) || 20,
    height: parseFloat(document.getElementById("param-height").value) || 10,
    min_step: parseStepValue(document.getElementById("param-min-step").value),
    max_step: parseStepValue(document.getElementById("param-max-step").value),
    line_width: parseFloat(document.getElementById("param-line-width").value) || 1.2,
    smoothing: parseFloat(document.getElementById("param-smoothing").value) || 0,
    font_label: parseInt(document.getElementById("param-font-label").value) || 35,
    font_tick: parseInt(document.getElementById("param-font-tick").value) || 35,
    font_legend: parseInt(document.getElementById("param-font-legend").value) || 43,
    dpi: parseInt(document.getElementById("param-dpi").value) || 300,
    show_legend: document.getElementById("param-legend").checked,
    show_grid: document.getElementById("param-grid").checked,
    show_range: document.getElementById("param-range") ? document.getElementById("param-range").checked : true,
    map_name: document.getElementById("param-map-name").value,
    agent_count: document.getElementById("param-agent-count").value,
    memo: document.getElementById("param-memo").value,
    category: document.getElementById("param-category").value,
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

async function apiReorderMethods(order) {
  await fetch(`/api/method/reorder`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: SESSION_ID, order }),
  });
}

async function apiClearAllFiles() {
  await fetch(`/api/files/clear-all`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: SESSION_ID }),
  });
}

async function apiGetPlotData() {
  const res = await fetch(`/api/plot-data?session_id=${SESSION_ID}`);
  return res.json();
}

// ── Add Method ───────────────────────────────────────────
async function addMethod() {
  const name = `${t('method_prefix')}${state.methods.length + 1}`;
  const data = await apiAddMethod(name);
  state.methods.push({
    id: data.method_id,
    name: data.name,
    color_index: data.color_index,
    color: COLORS[data.color_index % COLORS.length],
    files: [],
  });
  renderMethods();
  toast(t("method_added"), "success");
}

// ── Clear All Files ──────────────────────────────────────
async function clearAllFiles() {
  if (state.methods.length === 0) return;
  
  // どの手法にもファイルがない場合は何もしない
  let hasFiles = false;
  if (state.plotData && state.plotData.methods) {
    hasFiles = state.plotData.methods.some(m => m.file_count > 0);
  }
  if (!hasFiles) return;

  if (!confirm(t("confirm_clear_csvs"))) return;
  
  await apiClearAllFiles();
  
  await refreshPlotData();
  renderMethods();
  renderTabs();
  renderGraph();
  
  toast(t("csvs_cleared"), "success");
}

// ── Delete Method ────────────────────────────────────────
async function deleteMethod(methodId) {
  await apiDeleteMethod(methodId);
  state.methods = state.methods.filter(m => m.id !== methodId);
  await refreshPlotData();
  renderMethods();
  renderTabs();
  renderGraph();
  toast(t("method_deleted"), "info");
}

// ── Upload Files ─────────────────────────────────────────
async function uploadFiles(methodId, fileList) {
  const result = await apiUploadFiles(methodId, fileList);
  if (result.error) {
    toast(`${t("error_prefix")}${result.error}`, "error");
    return;
  }

  let successCount = 0;
  for (const r of result.results) {
    if (r.error) {
      toast(`${r.filename}: ${r.error}`, "error");
    } else {
      successCount++;
      if (r.warning) {
        toast(`${t("attention_prefix")}${r.filename} - ${r.warning}`, "warning");
      }
    }
  }
  if (successCount > 0) {
    toast(`${successCount}${t("files_added")}`, "success");
  }

  // Auto-fill map name and agent count from detected values (always update)
  if (result.map_name) {
    document.getElementById("param-map-name").value = result.map_name;
  }
  if (result.agent_count) {
    document.getElementById("param-agent-count").value = result.agent_count;
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

  state.methods.forEach((method, index) => {
    const card = document.createElement("div");
    card.className = "metric-card";
    card.id = `method-card-${method.id}`;
    
    // -- Drag and Drop --
    card.draggable = true;
    
    card.addEventListener("dragstart", (e) => {
      e.dataTransfer.effectAllowed = "move";
      e.dataTransfer.setData("text/plain", method.id);
      setTimeout(() => card.classList.add("dragging"), 0);
    });

    card.addEventListener("dragend", () => {
      card.classList.remove("dragging");
      document.querySelectorAll(".metric-card").forEach(c => {
        c.classList.remove("drag-over-top");
        c.classList.remove("drag-over-bottom");
      });
    });

    card.addEventListener("dragover", (e) => {
      e.preventDefault();
      e.dataTransfer.dropEffect = "move";
      
      const rect = card.getBoundingClientRect();
      const midPoint = rect.top + rect.height / 2;
      
      if (e.clientY < midPoint) {
        card.classList.add("drag-over-top");
        card.classList.remove("drag-over-bottom");
      } else {
        card.classList.add("drag-over-bottom");
        card.classList.remove("drag-over-top");
      }
    });

    card.addEventListener("dragleave", () => {
      card.classList.remove("drag-over-top");
      card.classList.remove("drag-over-bottom");
    });

    card.addEventListener("drop", async (e) => {
      e.preventDefault();
      card.classList.remove("drag-over-top");
      card.classList.remove("drag-over-bottom");
      
      const draggedId = e.dataTransfer.getData("text/plain");
      if (draggedId === method.id) return;
      
      const rect = card.getBoundingClientRect();
      const midPoint = rect.top + rect.height / 2;
      const insertAfter = e.clientY >= midPoint;
      
      const draggedIndex = state.methods.findIndex(m => m.id === draggedId);
      const targetIndex = state.methods.findIndex(m => m.id === method.id);
      
      if (draggedIndex === -1 || targetIndex === -1) return;
      
      // Reorder array
      const draggedItem = state.methods[draggedIndex];
      state.methods.splice(draggedIndex, 1);
      
      let newTargetIndex = state.methods.findIndex(m => m.id === method.id);
      if (insertAfter) newTargetIndex++;
      
      state.methods.splice(newTargetIndex, 0, draggedItem);
      
      // Sync with backend
      const newOrder = state.methods.map(m => m.id);
      await apiReorderMethods(newOrder);
      
      renderMethods();
      renderGraph();
    });

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

    // Drop zone
    const dropZone = document.createElement("div");
    dropZone.className = "drop-zone";
    const isExpanded = state.expandedMethods.has(method.id);
    dropZone.style.display = isExpanded ? "flex" : "none";
    swatchWrap.style.display = isExpanded ? "flex" : "none";
    
    const toggleBtn = document.createElement("button");
    toggleBtn.className = "metric-delete-btn";
    toggleBtn.innerHTML = isExpanded ? "▼" : "▶";
    toggleBtn.title = "開閉";
    toggleBtn.onclick = (e) => {
      e.stopPropagation();
      const isCollapsed = dropZone.style.display === "none";
      if (isCollapsed) {
        dropZone.style.display = "flex";
        swatchWrap.style.display = "flex";
        toggleBtn.innerHTML = "▼";
        state.expandedMethods.add(method.id);
      } else {
        dropZone.style.display = "none";
        swatchWrap.style.display = "none";
        toggleBtn.innerHTML = "▶";
        state.expandedMethods.delete(method.id);
      }
    };

    header.appendChild(dot);
    header.appendChild(nameInput);
    header.appendChild(toggleBtn);
    header.appendChild(delBtn);
    card.appendChild(header);
    card.appendChild(swatchWrap);

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
    uploadLabel.innerHTML = `${t("drop_csv")}`;
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
  // In legend output mode, all refresh paths render the legend preview instead.
  if (state.mode === "legend") {
    return renderLegendPreview();
  }
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

  // Per-metric legend position
  const ls = getLegendSetting(state.activeMetric);
  params.legend_auto = ls.auto;
  params.legend_x = ls.x;
  params.legend_y = ls.y;
  updateLegendControls();

  // Populate stats
  const statsContainer = document.getElementById("stats-container");
  const statsContent = document.getElementById("stats-content");
  if (statsContainer && statsContent) {
    let computedStats = [];
    if (metricData && metricData.series) {
      const groups = {};
      for (const s of metricData.series) {
        if (!groups[s.method_id]) {
          groups[s.method_id] = { name: s.method_name, color_index: s.color_index, series: [] };
        }
        groups[s.method_id].series.push(s);
      }
      for (const mid in groups) {
        const g = groups[mid];
        // 学習の最後10%区間で各run(シード)ごとに平均を出し、
        // その「run間」で標準偏差を取る(論文標準のシード間std)。
        // 1実行(n=1)では std は定義できないため null とする。
        const LAST_FRACTION = 0.10;
        const perRunMeans = [];
        for (const s of g.series) {
          let step = s.step;
          let value = s.value;
          if (params.max_step != null) {
            const fStep = [], fVal = [];
            for (let i = 0; i < step.length; i++) {
              if (step[i] <= params.max_step) {
                fStep.push(step[i]);
                fVal.push(value[i]);
              }
            }
            step = fStep;
            value = fVal;
          }
          if (step.length === 0) continue;
          const lo = step[0];
          const hi = step[step.length - 1];
          const threshold = hi - LAST_FRACTION * (hi - lo);
          let sum = 0, cnt = 0;
          for (let i = 0; i < step.length; i++) {
            if (step[i] >= threshold) { sum += value[i]; cnt++; }
          }
          if (cnt > 0) perRunMeans.push(sum / cnt);
        }
        if (perRunMeans.length > 0) {
          const mean = perRunMeans.reduce((a, b) => a + b, 0) / perRunMeans.length;
          let std = null;
          if (perRunMeans.length > 1) {
            // 標本標準偏差 (ddof=1): シード間ばらつきの推定として標準的
            const sqSum = perRunMeans.reduce((a, b) => a + (b - mean) ** 2, 0);
            std = Math.sqrt(sqSum / (perRunMeans.length - 1));
          }
          computedStats.push({
            method_id: mid,
            method_name: g.name,
            color_index: g.color_index,
            n_runs: perRunMeans.length,
            mean: mean,
            std: std
          });
        }
      }
    }

    // Order the stat cards to match the left method list (top to bottom)
    const methodOrder = new Map(state.methods.map((m, i) => [m.id, i]));
    computedStats.sort((a, b) =>
      (methodOrder.has(a.method_id) ? methodOrder.get(a.method_id) : Number.MAX_SAFE_INTEGER) -
      (methodOrder.has(b.method_id) ? methodOrder.get(b.method_id) : Number.MAX_SAFE_INTEGER));

    if (computedStats.length > 0) {
      statsContainer.style.display = "block";
      statsContent.innerHTML = "";
      computedStats.forEach(st => {
        const card = document.createElement("div");
        card.style.background = "var(--bg-base, #0c0e14)";
        card.style.border = "1px solid var(--border, rgba(148,163,184,.12))";
        card.style.borderRadius = "8px";
        card.style.padding = "10px 14px";
        card.style.minWidth = "0";

        const dot = document.createElement("span");
        dot.style.display = "inline-block";
        dot.style.width = "12px";
        dot.style.height = "12px";
        dot.style.borderRadius = "50%";
        dot.style.background = params.method_colors[st.method_id] || COLORS[st.color_index % COLORS.length];
        dot.style.marginRight = "8px";
        dot.style.flexShrink = "0";

        const title = document.createElement("div");
        title.style.display = "flex";
        title.style.alignItems = "center";
        title.style.fontWeight = "600";
        title.style.fontSize = "13px";
        title.style.color = "var(--text-primary, #f1f5f9)";
        title.style.marginBottom = "4px";
        title.style.overflow = "hidden";
        title.appendChild(dot);

        const nameSpan = document.createElement("span");
        nameSpan.style.overflow = "hidden";
        nameSpan.style.textOverflow = "ellipsis";
        nameSpan.style.whiteSpace = "nowrap";
        nameSpan.textContent = st.method_name;
        title.appendChild(nameSpan);

        if (st.n_runs > 1) {
          const span = document.createElement("span");
          span.style.fontSize = "11px";
          span.style.color = "var(--text-muted, #6b7280)";
          span.style.marginLeft = "6px";
          span.style.flexShrink = "0";
          span.textContent = `(${st.n_runs} runs)`;
          title.appendChild(span);
        }

        const val = document.createElement("div");
        val.style.fontSize = "14px";
        val.style.fontFamily = "monospace";
        val.style.color = "var(--text-secondary, #94a3b8)";
        val.textContent = (st.std != null)
          ? `${st.mean.toFixed(3)} ± ${st.std.toFixed(3)}`
          : `${st.mean.toFixed(3)}`;

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
    toast(t("no_graph"), "error");
    return;
  }

  const params = getParams();
  const metricData = state.plotData?.metrics?.find(m => m.metric === state.activeMetric);
  if (metricData) {
    params.y_label = metricData.y_label || "Value";
  }
  params.x_label = "Training steps";

  // Per-metric legend position
  const ls = getLegendSetting(state.activeMetric);
  params.legend_auto = ls.auto;
  params.legend_x = ls.x;
  params.legend_y = ls.y;

  toast(`${format.toUpperCase()} ${t("exporting")}`, "info");

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
      toast(`${t("error_prefix")}${err.error}`, "error");
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
    if (params.category) parts.push(params.category);
    if (params.memo) parts.push(params.memo);
    parts.push(state.activeMetric);
    parts.push(`${Math.round(params.width)}-${Math.round(params.height)}`);
    a.download = parts.join("_") + `.${format}`;
    a.click();
    URL.revokeObjectURL(url);
    toast(`${format.toUpperCase()} ${t("downloaded")}`, "success");
  } catch (e) {
    toast(`${t("export_failed")}${e.message}`, "error");
  }
}

// ── Legend output mode ───────────────────────────────────
// NOTE: state.methods[].files is NOT populated client-side; the server
// reports file counts via plotData.methods[].file_count. Use that to know
// which methods actually appear in the plots (and thus in the legend).
function methodsWithFiles() {
  if (!state.plotData || !state.plotData.methods) return [];
  return state.plotData.methods.filter(m => m.file_count > 0);
}

function setMode(mode) {
  state.mode = mode;
  const isLegend = mode === "legend";

  document.getElementById("mode-graph-btn").classList.toggle("active", !isLegend);
  document.getElementById("mode-legend-btn").classList.toggle("active", isLegend);

  // Toggle toolbars
  document.getElementById("tab-bar").style.display = isLegend ? "none" : "";
  document.getElementById("graph-export-buttons").style.display = isLegend ? "none" : "";
  document.getElementById("legend-toolbar").style.display = isLegend ? "flex" : "none";
  // The graph-only legend-position controls never apply in legend mode
  const posCtl = document.getElementById("legend-controls");
  if (posCtl && isLegend) posCtl.style.display = "none";
  // Stats are graph-only
  const stats = document.getElementById("stats-container");
  if (stats && isLegend) stats.style.display = "none";

  if (isLegend) {
    renderLegendPreview();
  } else {
    renderGraph();
  }
}

function onLegendControlChange() {
  // Show ncol input only when "列数指定" is selected
  const rows = document.getElementById("legend-rows").value;
  document.getElementById("legend-ncol-wrap").style.display =
    (rows === "manual") ? "" : "none";
  if (state.mode === "legend") renderLegendPreview();
}

function getLegendParams() {
  const params = getParams();  // shares method_colors, map_name, agent_count, memo, dpi
  const rows = document.getElementById("legend-rows").value;
  const ncolInput = parseInt(document.getElementById("legend-ncol").value) || 0;
  const orientation = document.getElementById("legend-orientation").value;

  // Resolve rows selection into ncol / max_per_row
  const nMethods = methodsWithFiles().length;
  if (orientation === "vertical") {
    params.legend_orientation = "vertical";
  } else {
    params.legend_orientation = "horizontal";
    if (rows === "1") {
      params.legend_ncol = Math.max(1, nMethods);
    } else if (rows === "2") {
      params.legend_ncol = Math.max(1, Math.ceil(nMethods / 2));
    } else if (rows === "manual") {
      params.legend_ncol = Math.max(1, ncolInput);
    } // "auto": leave unset → backend default (1 row, wraps to 2 when many)
  }
  params.legend_line_width = parseFloat(document.getElementById("legend-line-width").value) || 3;
  params.legend_font = parseInt(document.getElementById("legend-font").value) || 24;
  params.legend_frame = document.getElementById("legend-frame").checked;
  params.legend_transparent = document.getElementById("legend-transparent").checked;
  return params;
}

let currentLegendPreviewUrl = null;
async function renderLegendPreview() {
  const wrapper = document.getElementById("preview-wrapper");
  const imgData = document.getElementById("matplotlib-preview");
  const placeholder = document.getElementById("graph-placeholder");
  const loading = document.getElementById("loading-overlay");
  const stats = document.getElementById("stats-container");
  if (stats) stats.style.display = "none";

  if (methodsWithFiles().length === 0) {
    wrapper.style.display = "none";
    placeholder.style.display = "flex";
    return;
  }

  placeholder.style.display = "none";
  wrapper.style.display = "none";
  loading.style.display = "flex";

  try {
    const res = await fetch("/api/export-legend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: SESSION_ID,
        format: "png",
        params: getLegendParams(),
      }),
    });
    if (!res.ok) {
      const err = await res.json();
      toast(`${t("error_prefix")}${err.error}`, "error");
      loading.style.display = "none";
      return;
    }
    const blob = await res.blob();
    if (currentLegendPreviewUrl) URL.revokeObjectURL(currentLegendPreviewUrl);
    currentLegendPreviewUrl = URL.createObjectURL(blob);
    imgData.src = currentLegendPreviewUrl;
    loading.style.display = "none";
    wrapper.style.display = "flex";
  } catch (e) {
    toast(`${t("export_failed")}${e.message}`, "error");
    loading.style.display = "none";
  }
}

// ── Export Legend only (standalone file) ─────────────────
async function exportLegend(format) {
  if (methodsWithFiles().length === 0) {
    toast(t("no_export"), "error");
    return;
  }

  const params = getLegendParams();
  toast(`${format.toUpperCase()} ${t("exporting")}`, "info");

  try {
    const res = await fetch("/api/export-legend", {
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
      toast(`${t("error_prefix")}${err.error}`, "error");
      return;
    }

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    // Filename = whichever optional fields are filled, joined by "_", + "legend".
    // すべて任意: 空の項目は省略される。
    const parts = [];
    if (params.map_name) parts.push(params.map_name);
    if (params.agent_count) parts.push(`${params.agent_count}agent`);
    if (params.category) parts.push(params.category);
    if (params.memo) parts.push(params.memo);
    parts.push("legend");
    a.download = parts.join("_") + `.${format}`;
    a.click();
    URL.revokeObjectURL(url);
    toast(`${format.toUpperCase()} ${t("downloaded")}`, "success");
  } catch (e) {
    toast(`${t("export_failed")}${e.message}`, "error");
  }
}

// ── Export All (ZIP) ─────────────────────────────────────
async function exportAll(format) {
  if (!state.plotData || !state.plotData.metrics || state.plotData.metrics.length === 0) {
    toast(t("no_export"), "error");
    return;
  }

  const params = getParams();
  // Include all per-metric legend settings for batch export
  params.legend_settings = {};
  for (const metric in state.legendSettings) {
    params.legend_settings[metric] = state.legendSettings[metric];
  }
  toast(`${t("all_metrics")}${format.toUpperCase()}${t("batch_exporting")}`, "info");

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
      toast(`${t("error_prefix")}${err.error}`, "error");
      return;
    }

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    // Build filename: {map}_{agents}agent_all_metrics_{figsize}_{format}.zip
    const parts = [];
    if (params.map_name) parts.push(params.map_name);
    if (params.agent_count) parts.push(`${params.agent_count}agent`);
    if (params.memo) parts.push(params.memo);
    parts.push("all_metrics");
    parts.push(`${Math.round(params.width)}-${Math.round(params.height)}`);
    a.download = parts.join("_") + `_${format}.zip`;
    a.click();
    URL.revokeObjectURL(url);
    toast(`${state.plotData.metrics.length}${t("graphs_zip_downloaded")}`, "success");
  } catch (e) {
    toast(`${t("batch_export_failed")}${e.message}`, "error");
  }
}

// ── Export CSV (organized folders) ────────────────────────
async function exportCsvZip() {
  if (!state.plotData || !state.plotData.metrics || state.plotData.metrics.length === 0) {
    toast(t("no_export"), "error");
    return;
  }

  const params = getParams();
  // Colors are client-side only; send them by method name so the export can
  // save each method's color into its per-folder _meta.json.
  const colorsByName = {};
  state.methods.forEach(m => {
    colorsByName[m.name] = m.color || COLORS[m.color_index % COLORS.length];
  });
  toast(t("csv_exporting"), "info");

  try {
    const res = await fetch("/api/export-csv", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: SESSION_ID,
        map_name: params.map_name,
        agent_count: params.agent_count,
        category: params.category,
        memo: params.memo,
        colors_by_name: colorsByName,
      }),
    });

    if (!res.ok) {
      const err = await res.json();
      toast(`${t("error_prefix")}${err.error}`, "error");
      return;
    }

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    const parts = [];
    if (params.map_name) parts.push(params.map_name);
    if (params.agent_count) parts.push(`${params.agent_count}agent`);
    if (params.memo) parts.push(params.memo);
    parts.push("csv");
    a.download = parts.join("_") + ".zip";
    a.click();
    URL.revokeObjectURL(url);
    toast(t("csv_zip_downloaded"), "success");
  } catch (e) {
    toast(`${t("csv_export_failed")}${e.message}`, "error");
  }
}

// ── Import CSV Folder (exported structure) ───────────────
async function handleCsvFolderImport(event) {
  const files = event.target.files;
  if (!files || files.length === 0) return;

  // Group files by method name from folder structure
  // Expected: root/method_name/run_name/file.csv  (4 parts)
  //       or: root/method_name/file.csv            (3 parts)
  //       or: method_name/file.csv                 (2 parts, if immediate subfolders selected)
  const methodGroups = {};
  const metaFiles = [];  // root _meta.json manifest(s)
  let addedCount = 0;

  for (let i = 0; i < files.length; i++) {
    const file = files[i];

    const parts = file.webkitRelativePath.split('/');

    // Manifest at the root: {root}/_meta.json → holds all methods' color/order
    if (file.name === "_meta.json") {
      metaFiles.push(file);
      continue;
    }

    if (!file.name.endsWith('.csv') && !file.name.endsWith('.CSV')) continue;

    let methodName;
    if (parts.length >= 4) {
      // root/method/run/file.csv → method is parts[1]
      methodName = parts[1];
    } else if (parts.length === 3) {
      // root/method/file.csv → method is parts[1]
      methodName = parts[1];
    } else if (parts.length === 2) {
      // method/file.csv → method is parts[0]
      methodName = parts[0];
    } else {
      continue;
    }

    if (!methodGroups[methodName]) {
      methodGroups[methodName] = [];
    }
    methodGroups[methodName].push(file);
    addedCount++;
  }

  if (addedCount === 0) {
    toast(t("error_prefix") + "CSVファイルが見つかりません", "warning");
    event.target.value = "";
    return;
  }

  const loading = document.getElementById("loading-overlay");
  loading.style.display = "flex";
  toast(t("csv_folder_importing"), "info");

  try {
    for (const methodName in methodGroups) {
      let methodId = null;
      const existing = state.methods.find(m => m.name === methodName);
      if (existing) {
        methodId = existing.id;
      } else {
        const data = await apiAddMethod(methodName);
        methodId = data.method_id;
        state.methods.push({
          id: methodId,
          name: data.name,
          color_index: data.color_index,
          color: COLORS[data.color_index % COLORS.length],
          files: [],
        });
      }

      const result = await apiUploadFiles(methodId, methodGroups[methodName]);
      if (result.map_name) {
        document.getElementById("param-map-name").value = result.map_name;
      }
      if (result.agent_count) {
        document.getElementById("param-agent-count").value = result.agent_count;
      }
    }

    // Restore color + order from the root _meta.json manifest (if present)
    const metaByMethod = {};
    for (const file of metaFiles) {
      try {
        const obj = JSON.parse(await file.text());
        const list = Array.isArray(obj.methods) ? obj.methods
                   : (obj.name ? [obj] : []);  // tolerate a single-entry object
        for (const e of list) {
          if (e && e.name) metaByMethod[e.name] = e;
        }
      } catch (e) { /* ignore malformed _meta.json */ }
    }
    if (Object.keys(metaByMethod).length) {
      state.methods.forEach(m => {
        const meta = metaByMethod[m.name];
        if (meta && meta.color) m.color = meta.color;
      });
      const orderOf = (m) => {
        const o = metaByMethod[m.name] && metaByMethod[m.name].order;
        return (o === undefined || o === null) ? Number.MAX_SAFE_INTEGER : o;
      };
      state.methods.sort((a, b) => orderOf(a) - orderOf(b));
      await apiReorderMethods(state.methods.map(m => m.id));
    }

    toast(`${addedCount}${t("csv_folder_imported")}`, "success");
  } catch (err) {
    toast(`${t("error_prefix")}${err.message}`, "error");
  } finally {
    await refreshPlotData();
    renderMethods();
    renderTabs();
    renderGraph();
    loading.style.display = "none";
    event.target.value = "";
  }
}

// ── Auto-update graph on param change ────────────────────
document.querySelectorAll("#params-content input").forEach(el => {
  if (el.type === "range") return;  // sliders handled separately (debounced)
  const evts = el.type === "checkbox" ? ["change"] : ["change", "input"];
  evts.forEach(evt => el.addEventListener(evt, () => renderGraph()));
});
 
// ── Smoothing slider (TensorBoard-style EMA) ─────────────
// Debounced so dragging doesn't flood the server with preview renders.
(function initSmoothingSlider() {
  const slider = document.getElementById("param-smoothing");
  const label = document.getElementById("smoothing-value");
  if (!slider) return;
  let debounce;
  slider.addEventListener("input", () => {
    if (label) label.textContent = parseFloat(slider.value).toFixed(3);
    clearTimeout(debounce);
    debounce = setTimeout(() => renderGraph(), 150);
  });
})();

// ── Legend Position (per-metric) ─────────────────────────
function getLegendSetting(metric) {
  if (!state.legendSettings[metric]) {
    state.legendSettings[metric] = { auto: true, x: 1.0, y: 1.0 };
  }
  return state.legendSettings[metric];
}

function adjustLegend(direction) {
  if (!state.activeMetric) return;
  const setting = getLegendSetting(state.activeMetric);
  const step = 0.05;
  if (setting.auto) {
    setting.auto = false;
    setting.x = 1.0;
    setting.y = 1.0;
  }
  switch (direction) {
    case 'up':    setting.y += step; break;
    case 'down':  setting.y -= step; break;
    case 'left':  setting.x -= step; break;
    case 'right': setting.x += step; break;
  }
  // Round to avoid floating point drift
  setting.x = Math.round(setting.x * 100) / 100;
  setting.y = Math.round(setting.y * 100) / 100;
  updateLegendControls();
  renderGraph();
}

function resetLegend() {
  if (!state.activeMetric) return;
  state.legendSettings[state.activeMetric] = { auto: true, x: 1.0, y: 1.0 };
  updateLegendControls();
  renderGraph();
}

function updateLegendControls() {
  const controls = document.getElementById('legend-controls');
  const display = document.getElementById('legend-pos-display');
  if (!controls) return;

  const showLegend = document.getElementById('param-legend').checked;
  if (!state.activeMetric || !showLegend ||
      !state.plotData || !state.plotData.metrics || state.plotData.metrics.length === 0) {
    controls.style.display = 'none';
    return;
  }
  controls.style.display = 'flex';
  const setting = getLegendSetting(state.activeMetric);
  if (setting.auto) {
    display.textContent = t('legend_auto');
  } else {
    display.textContent = `(${setting.x.toFixed(2)}, ${setting.y.toFixed(2)})`;
  }
}

// ── Initialize ───────────────────────────────────────────
async function init() {
  const data = await apiGetPlotData();
  
  if (data && data.methods) {
    state.methods = data.methods.map(m => ({
      id: m.id,
      name: m.name,
      color_index: m.color_index,
      color: m.color || COLORS[m.color_index % COLORS.length],
      files: [] // files logic will be rehydrated via refreshPlotData if needed
    }));
  }

  await refreshPlotData();
  renderMethods();
  renderTabs();
  renderGraph();
}

init();
