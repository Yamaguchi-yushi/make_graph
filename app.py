"""
CSVグラフ可視化UIアプリケーション
Flask + Plotly.js によるインタラクティブなグラフ描画

ワークフロー:
  1. ユーザーが「手法」(method) を追加（例: 従来手法, 提案手法）
  2. 各手法にCSVファイルをアップロード
  3. ファイル名からメトリクス名を自動検出 (-tag-XXX パターン)
  4. メトリクスごとにグラフを自動生成（各手法の線が1つのグラフに表示）
"""

import os
import io
import re
import uuid
import json
import zipfile
from flask import Flask, render_template, request, jsonify, send_file

import pandas as pd
import matplotlib
# Cairo backend (same as original script) with Agg fallback
try:
    matplotlib.use("module://matplotlib.backends.backend_cairo")
except Exception:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams

# ── Japanese font setup (identical to original script) ───
_font_found = False
for _name in ["Hiragino Sans", "Hiragino Kaku Gothic Pro",
              "Noto Sans CJK JP", "Yu Gothic", "IPAexGothic", "TakaoPGothic"]:
    if any(_name in f.name for f in font_manager.fontManager.ttflist):
        rcParams["font.family"] = _name
        _font_found = True
        break

if not _font_found:
    jp_fonts = [f for f in font_manager.fontManager.ttflist
                if any(n in f.name for n in
                       ['Gothic', 'Hiragino', 'Noto', 'IPA', 'Takao', 'Meiryo'])]
    if jp_fonts:
        rcParams["font.family"] = jp_fonts[0].name

rcParams["axes.unicode_minus"] = False
rcParams["pdf.fonttype"] = 3
rcParams["ps.fonttype"] = 3

# ── Default rcParams matching original script ────────────
DEFAULT_RCPARAMS = {
    "font.size": 18,
    "axes.titlesize": 24,
    "axes.labelsize": 30,
    "xtick.labelsize": 25,
    "ytick.labelsize": 25,
    "legend.fontsize": 30,
    "legend.title_fontsize": 20,
}
for k, v in DEFAULT_RCPARAMS.items():
    rcParams[k] = v

# Original script colors (色覚多様性対応)
DEFAULT_COLORS = ["#03AF7A", "#005AFF", "red", "#4DC4FF", "#F6AA00", "#FFF100"]

# Y-axis label mapping (same as original script)
METRIC_Y_LABELS = {
    "goal": "Goal rate",
    "collision": "Collision rate",
    "timeup": "Timeup rate",
    "timeout": "Timeup rate",
    "success": "Success rate",
    "episode_len": "Episode length",
    "reward": "Reward",
    "cost": "Cost",
    "rate": "Rate",
    "ratio": "Rate",
}

# ── Flask App ─────────────────────────────────────────────
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024 * 1024  # 64 MB

# In-memory store
# session -> { methods: [ {id, name, color_index, files: [{id, filename, metric, step, value}]} ] }
sessions: dict = {}
DEFAULT_SESSION = "default"


def _ensure_session(sid: str):
    if sid not in sessions:
        sessions[sid] = {"methods": [], "map_name": "", "agent_count": ""}
    return sessions[sid]


def detect_metric(filename: str) -> str:
    """ファイル名からメトリクス名を検出 (-tag-XXX パターン)"""
    name_noext = os.path.splitext(filename)[0]
    pos = name_noext.find("-tag-")
    if pos != -1:
        rest = name_noext[pos + len("-tag-"):]
        m = re.match(r"([A-Za-z0-9_]+)", rest)
        if m:
            return m.group(1).rstrip("_")
    return "unknown"


def extract_map_name(filename: str) -> str:
    """ファイル名からマップ名を抽出 (元のスクリプトと同じ)"""
    m = re.search(r"map_([a-zA-Z0-9xX]+)-v\d+", filename)
    if m:
        v = re.search(r"-v(\d+)", filename)
        return m.group(1) + "-v" + v.group(1) if v else m.group(1)
    return ""


def extract_agent_count(filename: str) -> str:
    """ファイル名からエージェント数を抽出 (元のスクリプトと同じ)"""
    m = re.search(r"(\d+)agent", filename)
    return m.group(1) if m else ""


def get_y_label(metric: str) -> str:
    """メトリクス名からY軸ラベルを返す（元のスクリプトと同じロジック）"""
    ml = metric.lower()
    for key, label in METRIC_Y_LABELS.items():
        if key in ml:
            return label
    return "Value"


def load_csv_data(file_bytes: bytes):
    """CSVファイルを読み込み、step と value の配列を返す"""
    df = pd.read_csv(io.BytesIO(file_bytes))
    cols_lower = [c.lower() for c in df.columns]

    step_col = None
    for i, c in enumerate(cols_lower):
        if c in ["step", "steps", "global_step", "t", "x"]:
            step_col = df.columns[i]
            break
    if step_col is None:
        step_col = df.columns[1] if df.shape[1] >= 2 else df.columns[0]

    value_col = None
    for i, c in enumerate(cols_lower):
        if c in ["value", "mean", "y", "score", "metric"]:
            value_col = df.columns[i]
            break
    if value_col is None:
        value_col = df.columns[-1]

    step = df[step_col].dropna().tolist()
    value = df[value_col].dropna().tolist()
    min_len = min(len(step), len(value))
    return step[:min_len], value[:min_len]


# ── Routes ────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/method", methods=["POST"])
def add_method():
    """手法を追加"""
    data = request.get_json(force=True)
    sid = data.get("session_id", DEFAULT_SESSION)
    name = data.get("name", "手法")

    session = _ensure_session(sid)
    mid = str(uuid.uuid4())[:8]
    color_index = len(session["methods"])
    session["methods"].append({
        "id": mid,
        "name": name,
        "color_index": color_index,
        "files": [],
    })
    return jsonify({"method_id": mid, "name": name, "color_index": color_index})


@app.route("/api/method/<method_id>", methods=["DELETE"])
def delete_method(method_id):
    """手法を削除"""
    sid = request.args.get("session_id", DEFAULT_SESSION)
    session = _ensure_session(sid)
    session["methods"] = [m for m in session["methods"] if m["id"] != method_id]
    return jsonify({"ok": True})


@app.route("/api/method/<method_id>/name", methods=["POST"])
def update_method_name(method_id):
    """手法名を更新"""
    data = request.get_json(force=True)
    sid = data.get("session_id", DEFAULT_SESSION)
    new_name = data.get("name", "")

    session = _ensure_session(sid)
    for m in session["methods"]:
        if m["id"] == method_id:
            m["name"] = new_name
            return jsonify({"ok": True})
    return jsonify({"error": "not found"}), 404


@app.route("/api/upload", methods=["POST"])
def upload_csv():
    """CSVファイルをアップロード（手法に紐付け）"""
    sid = request.form.get("session_id", DEFAULT_SESSION)
    method_id = request.form.get("method_id", "")
    files = request.files.getlist("files")

    if not files:
        return jsonify({"error": "ファイルが指定されていません"}), 400

    session = _ensure_session(sid)
    target = None
    for m in session["methods"]:
        if m["id"] == method_id:
            target = m
            break
    if target is None:
        return jsonify({"error": "手法が見つかりません"}), 404

    results = []
    detected_map = ""
    detected_agents = ""
    for file in files:
        filename = file.filename
        file_bytes = file.read()
        try:
            step, value = load_csv_data(file_bytes)
        except Exception as e:
            results.append({"filename": filename, "error": str(e)})
            continue

        metric = detect_metric(filename)
        file_id = str(uuid.uuid4())[:8]
        target["files"].append({
            "id": file_id,
            "filename": filename,
            "metric": metric,
            "step": step,
            "value": value,
        })
        results.append({
            "file_id": file_id,
            "filename": filename,
            "metric": metric,
            "points": len(step),
        })

        # Auto-detect map name and agent count from first file
        if not detected_map:
            detected_map = extract_map_name(filename)
        if not detected_agents:
            detected_agents = extract_agent_count(filename)

    # Store detected values (only if session doesn't already have them)
    if detected_map and not session.get("map_name"):
        session["map_name"] = detected_map
    if detected_agents and not session.get("agent_count"):
        session["agent_count"] = detected_agents

    return jsonify({
        "results": results,
        "map_name": session.get("map_name", ""),
        "agent_count": session.get("agent_count", ""),
    })


@app.route("/api/method/<method_id>/file/<file_id>", methods=["DELETE"])
def delete_file(method_id, file_id):
    """ファイルを削除"""
    sid = request.args.get("session_id", DEFAULT_SESSION)
    session = _ensure_session(sid)
    for m in session["methods"]:
        if m["id"] == method_id:
            m["files"] = [f for f in m["files"] if f["id"] != file_id]
            break
    return jsonify({"ok": True})


@app.route("/api/plot-data", methods=["GET"])
def get_plot_data():
    """メトリクスごとにグループ化したデータを返す"""
    sid = request.args.get("session_id", DEFAULT_SESSION)
    session = _ensure_session(sid)

    # メトリクスごとにデータを収集
    metrics_data: dict = {}  # metric -> [ {method_name, method_id, color_index, step, value} ]
    for method in session["methods"]:
        for f in method["files"]:
            metric = f["metric"]
            if metric not in metrics_data:
                metrics_data[metric] = []
            metrics_data[metric].append({
                "method_name": method["name"],
                "method_id": method["id"],
                "color_index": method["color_index"],
                "file_id": f["id"],
                "filename": f["filename"],
                "step": f["step"],
                "value": f["value"],
            })

    # preferred order
    preferred = ["collision_mean", "goal_mean", "goal_rate", "timeup_mean",
                 "timeout_rate", "cost_mean", "cost", "success_rate", "reward", "episode_len"]
    ordered_metrics = [m for m in preferred if m in metrics_data]
    ordered_metrics += [m for m in metrics_data if m not in ordered_metrics]

    result = []
    for metric in ordered_metrics:
        result.append({
            "metric": metric,
            "y_label": get_y_label(metric),
            "series": metrics_data[metric],
        })

    return jsonify({
        "metrics": result,
        "methods": [{"id": m["id"], "name": m["name"], "color_index": m["color_index"],
                      "file_count": len(m["files"])} for m in session["methods"]],
        "map_name": session.get("map_name", ""),
        "agent_count": session.get("agent_count", ""),
    })


@app.route("/api/update-session", methods=["POST"])
def update_session():
    """セッション情報（マップ名・エージェント数）を更新"""
    data = request.get_json(force=True)
    sid = data.get("session_id", DEFAULT_SESSION)
    session = _ensure_session(sid)
    if "map_name" in data:
        session["map_name"] = data["map_name"]
    if "agent_count" in data:
        session["agent_count"] = data["agent_count"]
    return jsonify({"ok": True})


@app.route("/api/export", methods=["POST"])
def export_graph():
    """Matplotlibで高品質画像をエクスポート（元のスクリプトと同一出力）"""
    data = request.get_json(force=True)
    sid = data.get("session_id", DEFAULT_SESSION)
    metric = data.get("metric", "")
    fmt = data.get("format", "png")
    params = data.get("params", {})

    session = _ensure_session(sid)

    # メトリクスのデータを収集
    series_list = []
    for method in session["methods"]:
        for f in method["files"]:
            if f["metric"] == metric:
                series_list.append({
                    "label": method["name"],
                    "method_id": method["id"],
                    "color_index": method["color_index"],
                    "step": f["step"],
                    "value": f["value"],
                })

    if not series_list:
        return jsonify({"error": "データがありません"}), 400

    # Set y_label for the metric
    params["y_label"] = params.get("y_label", get_y_label(metric))
    params["x_label"] = params.get("x_label", "Training steps")

    buf = _render_graph_to_buf(series_list, params, fmt)

    mime = {"png": "image/png", "pdf": "application/pdf", "eps": "application/postscript"}
    # Build filename: {map_name}_{agent_count}agent_{metric}_{figsize}.{fmt}
    download_name = _build_filename(params, session, metric, fmt)
    return send_file(
        buf,
        mimetype=mime.get(fmt, "application/octet-stream"),
        as_attachment=True,
        download_name=download_name,
    )


def _build_filename(params, session, metric, fmt):
    fig_w = params.get("width", 10)
    fig_h = params.get("height", 7.5)
    map_name = params.get("map_name", session.get("map_name", "unknown"))
    agent_count = params.get("agent_count", session.get("agent_count", ""))
    figsize_str = f"{int(fig_w)}-{int(fig_h)}"
    parts = []
    if map_name:
        parts.append(map_name)
    if agent_count:
        parts.append(f"{agent_count}agent")
    parts.append(metric)
    parts.append(figsize_str)
    return "_".join(parts) + f".{fmt}"


def _render_graph_to_buf(series_list, params, fmt):
    """Render a matplotlib graph to a BytesIO buffer."""
    fig_w = params.get("width", 10)
    fig_h = params.get("height", 7.5)
    dpi = params.get("dpi", 300)
    x_label = params.get("x_label", "Training steps")
    y_label = params.get("y_label", "Value")
    min_step = params.get("min_step")
    max_step = params.get("max_step")
    show_legend = params.get("show_legend", True)
    line_width = params.get("line_width", 1.2)
    font_label = params.get("font_label", 30)
    font_tick = params.get("font_tick", 25)
    font_legend = params.get("font_legend", 30)
    method_colors = params.get("method_colors", {})
    show_grid = params.get("show_grid", True)

    rcParams["font.size"] = 18
    rcParams["axes.titlesize"] = font_label
    rcParams["axes.labelsize"] = font_label
    rcParams["xtick.labelsize"] = font_tick
    rcParams["ytick.labelsize"] = font_tick
    rcParams["legend.fontsize"] = font_legend
    rcParams["legend.title_fontsize"] = int(font_legend * 0.7)

    fig, ax = plt.subplots(1, 1, figsize=(fig_w, fig_h))

    for s in series_list:
        step = s["step"]
        value = s["value"]
        if min_step is not None or max_step is not None:
            filtered = [(st, v) for st, v in zip(step, value)
                        if (min_step is None or st >= min_step) and
                           (max_step is None or st <= max_step)]
            if filtered:
                step, value = zip(*filtered)
            else:
                continue
        mid = s.get("method_id", "")
        color = method_colors.get(mid, DEFAULT_COLORS[s["color_index"] % len(DEFAULT_COLORS)])
        ax.plot(step, value, linewidth=line_width, label=s["label"], color=color)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    if show_grid:
        ax.grid(True, alpha=0.3)
    if show_legend:
        ax.legend(loc="best", framealpha=0.9)
    plt.tight_layout()

    buf = io.BytesIO()
    save_kwargs = {"bbox_inches": "tight"}
    if fmt == "png":
        save_kwargs["dpi"] = dpi
    fig.savefig(buf, format=fmt, **save_kwargs)
    plt.close(fig)
    buf.seek(0)
    return buf


@app.route("/api/export-all", methods=["POST"])
def export_all_graphs():
    """全メトリクスのグラフを一括ZIPダウンロード"""
    data = request.get_json(force=True)
    sid = data.get("session_id", DEFAULT_SESSION)
    fmt = data.get("format", "png")
    params = data.get("params", {})
    session = _ensure_session(sid)

    if not session["methods"]:
        return jsonify({"error": "データがありません"}), 400

    # Collect all metrics
    all_metrics = {}
    for method in session["methods"]:
        for f in method["files"]:
            metric = f["metric"]
            if metric not in all_metrics:
                all_metrics[metric] = {"y_label": get_y_label(metric), "series": []}
            all_metrics[metric]["series"].append({
                "label": method["name"],
                "method_id": method["id"],
                "color_index": method["color_index"],
                "step": f["step"],
                "value": f["value"],
            })

    if not all_metrics:
        return jsonify({"error": "メトリクスが見つかりません"}), 400

    # Build ZIP
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for metric, mdata in all_metrics.items():
            p = dict(params)
            p["y_label"] = mdata["y_label"]
            p["x_label"] = "Training steps"
            graph_buf = _render_graph_to_buf(mdata["series"], p, fmt)
            filename = _build_filename(params, session, metric, fmt)
            zf.writestr(filename, graph_buf.getvalue())

    zip_buf.seek(0)
    map_name = params.get("map_name", session.get("map_name", "graphs"))
    agent_count = params.get("agent_count", session.get("agent_count", ""))
    zip_parts = []
    if map_name:
        zip_parts.append(map_name)
    if agent_count:
        zip_parts.append(f"{agent_count}agent")
    zip_parts.append("all_metrics")
    zip_name = "_".join(zip_parts) + ".zip"

    return send_file(
        zip_buf,
        mimetype="application/zip",
        as_attachment=True,
        download_name=zip_name,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
