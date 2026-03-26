import re

html_path = "templates/index.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Update Width & Height
html = re.sub(r'(id="param-width" value=")[^"]+(")', r'\g<1>20\g<2>', html)
html = re.sub(r'(id="param-height" value=")[^"]+(")', r'\g<1>10\g<2>', html)

# Add Toggle Button
header_target = '<p class="subtitle">CSVファイルからインタラクティブなグラフを作成</p>'
header_replace = '<p class="subtitle" data-i18n="subtitle">CSVファイルからインタラクティブなグラフを作成</p>\n      </div>\n      <div class="header-right" style="margin-left: auto;">\n        <button id="lang-toggle-btn" class="btn btn-ghost btn-sm" onclick="toggleLanguage()" data-i18n="toggle_lang">English</button>'
html = html.replace('        <p class="subtitle">CSVファイルからインタラクティブなグラフを作成</p>\n      </div>', '        ' + header_replace + '\n      </div>')

# Add data-i18n tags
replacements = {
    '<h2><span class="icon">⚙️</span> グラフ設定</h2>': '<h2 data-i18n="settings"><span class="icon">⚙️</span> グラフ設定</h2>',
    '<label for="param-map-name">マップ名</label>': '<label for="param-map-name" data-i18n="map_name">マップ名</label>',
    'placeholder="自動検出"': 'placeholder="自動検出" data-i18n="auto_detect"',
    '<label for="param-agent-count">エージェント数</label>': '<label for="param-agent-count" data-i18n="agent_count">エージェント数</label>',
    '<label for="param-width">幅</label>': '<label for="param-width" data-i18n="width">幅</label>',
    '<label for="param-height">高さ</label>': '<label for="param-height" data-i18n="height">高さ</label>',
    '<label for="param-min-step">ステップ最小</label>': '<label for="param-min-step" data-i18n="step_min">ステップ最小</label>',
    '<label for="param-max-step">ステップ最大</label>': '<label for="param-max-step" data-i18n="step_max">ステップ最大</label>',
    'placeholder="例: 0, 1M"': 'placeholder="例: 0, 1M" data-i18n="ex_step_min"',
    'placeholder="例: 8M"': 'placeholder="例: 8M" data-i18n="ex_step_max"',
    '<label for="param-font-label">軸ラベル</label>': '<label for="param-font-label" data-i18n="axis_label">軸ラベル</label>',
    '<label for="param-font-tick">軸の数値</label>': '<label for="param-font-tick" data-i18n="axis_tick">軸の数値</label>',
    '<label for="param-font-legend">凡例</label>': '<label for="param-font-legend" data-i18n="legend_size">凡例</label>',
    '凡例を表示': '<span data-i18n="show_legend">凡例を表示</span>',
    'グリッド\n                </label>': '<span data-i18n="show_grid">グリッド</span>\n                </label>',
    '<h2><span class="icon">🔬</span> 手法</h2>': '<h2 data-i18n="methods"><span class="icon">🔬</span> 手法</h2>',
    '<span>＋ 手法追加</span>': '<span data-i18n="add_method">＋ 手法追加</span>',
    '<div class="empty-state" id="empty-state">': '<div class="empty-state" id="empty-state" data-i18n="empty_methods">',
    '<span>📦 PNG全保存</span>': '<span data-i18n="export_all_png">📦 PNG全保存</span>',
    '<span>📦 PDF全保存</span>': '<span data-i18n="export_all_pdf">📦 PDF全保存</span>',
    '<span>📦 EPS全保存</span>': '<span data-i18n="export_all_eps">📦 EPS全保存</span>',
    '<p>指標を追加してCSVファイルをアップロードすると<br>ここにグラフが表示されます</p>': '<p data-i18n="graph_placeholder">指標を追加してCSVファイルをアップロードすると<br>ここにグラフが表示されます</p>',
    '<p>画像を生成中...</p>': '<p data-i18n="generating">画像を生成中...</p>',
    '📊 最終パフォーマンス (最後1万ステップの平均 ± 標準偏差)</h3>': '📊 最終パフォーマンス (最後1万ステップの平均 ± 標準偏差)</h3>'
}
for k, v in replacements.items():
    html = html.replace(k, v)

html = re.sub(r'(<h3[^>]*>)\n?\s*📊 最終パフォーマンス \(最後1万ステップの平均 ± 標準偏差\)</h3>', r'\1<span data-i18n="final_perf">📊 最終パフォーマンス (最後1万ステップの平均 ± 標準偏差)</span></h3>', html)


with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)


js_path = "static/app.js"
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

i18n_code = """
const i18n = {
  ja: {
    "title": "Graph Visualizer — CSV可視化ツール",
    "subtitle": "CSVファイルからインタラクティブなグラフを作成",
    "settings": "⚙️ グラフ設定",
    "map_name": "マップ名",
    "agent_count": "エージェント数",
    "auto_detect": "自動検出",
    "width": "幅",
    "height": "高さ",
    "step_min": "ステップ最小",
    "step_max": "ステップ最大",
    "ex_step_min": "例: 0, 1M",
    "ex_step_max": "例: 8M",
    "axis_label": "軸ラベル",
    "axis_tick": "軸の数値",
    "legend_size": "凡例",
    "show_legend": "凡例を表示",
    "show_grid": "グリッド",
    "methods": "🔬 手法",
    "add_method": "＋ 手法追加",
    "empty_methods": "「＋ 手法追加」ボタンで<br>手法を追加してください<br><small>例: 従来手法, 提案手法, 関連研究</small>",
    "export_all_png": "📦 PNG全保存",
    "export_all_pdf": "📦 PDF全保存",
    "export_all_eps": "📦 EPS全保存",
    "graph_placeholder": "指標を追加してCSVファイルをアップロードすると<br>ここにグラフが表示されます",
    "generating": "画像を生成中...",
    "final_perf": "📊 最終パフォーマンス (最後1万ステップの平均 ± 標準偏差)",
    "toggle_lang": "English",
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
    "batch_export_failed": "一括エクスポート失敗: "
  },
  en: {
    "title": "Graph Visualizer",
    "subtitle": "Create interactive graphs from CSV files",
    "settings": "⚙️ Graph Settings",
    "map_name": "Map Name",
    "agent_count": "Agents",
    "auto_detect": "Auto-detect",
    "width": "Width",
    "height": "Height",
    "step_min": "Min Step",
    "step_max": "Max Step",
    "ex_step_min": "e.g., 0, 1M",
    "ex_step_max": "e.g., 8M",
    "axis_label": "Axis Label Size",
    "axis_tick": "Tick Size",
    "legend_size": "Legend Size",
    "show_legend": "Show Legend",
    "show_grid": "Show Grid",
    "methods": "🔬 Methods",
    "add_method": "＋ Add Method",
    "empty_methods": "Click \"＋ Add Method\" to add a method<br><small>e.g., Baseline, Proposed, Related Work</small>",
    "export_all_png": "📦 Export All PNG",
    "export_all_pdf": "📦 Export All PDF",
    "export_all_eps": "📦 Export All EPS",
    "graph_placeholder": "Add a method and upload CSV files<br>to display the graph here",
    "generating": "Generating image...",
    "final_perf": "📊 Final Performance (Last 10k steps Mean ± STD)",
    "toggle_lang": "日本語",
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
    "batch_export_failed": "Batch export failed: "
  }
};
let currentLang = localStorage.getItem("lang") || "ja";

function t(key) {
  return i18n[currentLang][key] || key;
}

function toggleLanguage() {
  currentLang = currentLang === "ja" ? "en" : "ja";
  localStorage.setItem("lang", currentLang);
  applyTranslations();
  renderMethods();
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
  document.title = t("title");
}
// Init translations on load
document.addEventListener("DOMContentLoaded", applyTranslations);
"""
if "const i18n =" not in js:
    js = i18n_code + "\n" + js

js = js.replace('width: parseFloat(document.getElementById("param-width").value) || 10', 'width: parseFloat(document.getElementById("param-width").value) || 20')
js = js.replace('height: parseFloat(document.getElementById("param-height").value) || 7.5', 'height: parseFloat(document.getElementById("param-height").value) || 10')
js = js.replace('`手法 ${state.methods.length + 1}`', '`${t(\'method_prefix\')}${state.methods.length + 1}`')
js = js.replace('toast("手法を追加しました", "success");', 'toast(t("method_added"), "success");')
js = js.replace('toast("手法を削除しました", "info");', 'toast(t("method_deleted"), "info");')
js = js.replace('toast(`エラー: ${result.error}`, "error");', 'toast(`${t("error_prefix")}${result.error}`, "error");')
js = js.replace('toast(`${r.filename}: ${r.error}`, "error");', 'toast(`${r.filename}: ${r.error}`, "error");')
js = js.replace('toast(`⚠️ 注意: ${r.filename} - ${r.warning}`, "warning");', 'toast(`${t("attention_prefix")}${r.filename} - ${r.warning}`, "warning");')
js = js.replace('toast(`${successCount}個のファイルを追加しました`, "success");', 'toast(`${successCount}${t("files_added")}`, "success");')
js = js.replace('<span>📁</span> CSVファイルをドラッグ＆ドロップ', '${t("drop_csv")}')
js = js.replace('toast("グラフが表示されていません", "error");', 'toast(t("no_graph"), "error");')
js = js.replace('toast(`${format.toUpperCase()} エクスポート中...`, "info");', 'toast(`${format.toUpperCase()} ${t("exporting")}`, "info");')
js = js.replace('toast(`${format.toUpperCase()} をダウンロードしました`, "success");', 'toast(`${format.toUpperCase()} ${t("downloaded")}`, "success");')
js = js.replace('toast(`エラー: ${err.error}`, "error");', 'toast(`${t("error_prefix")}${err.error}`, "error");')
js = js.replace('toast(`エクスポート失敗: ${e.message}`, "error");', 'toast(`${t("export_failed")}${e.message}`, "error");')
js = js.replace('toast("エクスポートするグラフがありません", "error");', 'toast(t("no_export"), "error");')
js = js.replace('toast(`全メトリクス ${format.toUpperCase()} 一括エクスポート中...`, "info");', 'toast(`${t("all_metrics")}${format.toUpperCase()}${t("batch_exporting")}`, "info");')
js = js.replace('toast(`${state.plotData.metrics.length}件のグラフをZIPでダウンロードしました`, "success");', 'toast(`${state.plotData.metrics.length}${t("graphs_zip_downloaded")}`, "success");')
js = js.replace('toast(`一括エクスポート失敗: ${e.message}`, "error");', 'toast(`${t("batch_export_failed")}${e.message}`, "error");')

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js)

print("Done updating index.html and app.js")
