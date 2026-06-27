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
import numpy as np

import pandas as pd
import matplotlib
# Cairo backend (same as original script) with Agg fallback.
# NOTE: matplotlib.use() for a module backend is LAZY — it does not raise even
# when pycairo/cairocffi are missing; the failure only surfaces later at render
# time (plt.subplots / savefig). So a plain try/except around use() never
# catches it, and a fresh `pip install -r requirements.txt` (which has no
# pycairo) crashes preview/export with
#   "cairo backend requires that pycairo>=1.14.0 or cairocffi is installed".
# We probe the actual dependency up front and fall back to Agg, which produces
# equivalent PNG/PDF/EPS output for these plots.
try:
    import cairo  # noqa: F401  (pycairo)
    _has_cairo = True
except ImportError:
    try:
        import cairocffi  # noqa: F401
        _has_cairo = True
    except ImportError:
        _has_cairo = False

if _has_cairo:
    matplotlib.use("module://matplotlib.backends.backend_cairo")
else:
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
    "axes.labelsize": 35,
    "xtick.labelsize": 35,
    "ytick.labelsize": 35,
    "legend.fontsize": 43,
    "legend.title_fontsize": 20,
}
for k, v in DEFAULT_RCPARAMS.items():
    rcParams[k] = v

# Original script colors (色覚多様性対応)
DEFAULT_COLORS = ["#03AF7A", "#005AFF", "red", "#4DC4FF", "#F6AA00", "#FFF100"]

# Y-axis label mapping (same as original script)
# NOTE: keys are matched in order via substring search, so put more specific
# keys (e.g. "task_completion") before generic ones (e.g. "rate").
METRIC_Y_LABELS = {
    "task_completion": "Task Completion",
    "completion": "Task Completion",
    "task": "Task Completion",
    "goal": "Goal Rate",
    "collision": "Collision Rate",
    "timeup": "Timeup Rate",
    "timeout": "Timeup Rate",
    "success": "Success Rate",
    "episode_len": "Episode Length",
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
    """ファイル名からマップ名を抽出 (改善版: _などを含むマップ名にも対応)"""
    m = re.search(r"map_(.+?)(?:_\d{4}-\d{2}-\d{2}|-tag-|\.csv)", filename)
    if m:
        return m.group(1)
    m2 = re.search(r"map_([a-zA-Z0-9xX_-]+)", filename)
    if m2:
        return m2.group(1)
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

def _smooth_ema(values, weight):
    """TensorBoardと同じEMA(指数移動平均)による平滑化.
 
    S_t = w * S_{t-1} + (1 - w) * X_t をデバイアス補正(1 - w^t で除算)付きで適用する。
    weight は 0〜1 未満。0 のときは平滑化なし(元の値をそのまま返す)。
    """
    if not weight or weight <= 0:
        return values
    smoothed = []
    last = 0.0
    num_acc = 0
    for v in values:
        if v is None or not np.isfinite(v):
            smoothed.append(v)
            continue
        last = last * weight + (1.0 - weight) * v
        num_acc += 1
        debias = 1.0 - weight ** num_acc
        smoothed.append(last / debias if debias > 0 else last)
    return smoothed
 


def _aggregate_series(series_list):
    """同一method_idのseriesをグルーピングし、複数ある場合は平均+min/max rangeに集約する。
    
    1本だけの場合はそのまま返す（aggregated=False）。
    複数ある場合は共通step軸に補間してmean/min/maxを算出（aggregated=True）。
    """
    from collections import defaultdict
    groups = defaultdict(list)
    for s in series_list:
        groups[s.get("method_id", s.get("label", ""))].append(s)

    result = []
    for mid, items in groups.items():
        if len(items) == 1:
            items[0]["aggregated"] = False
            result.append(items[0])
        else:
            # 全seriesのstep範囲のunionを作り、共通step軸に補間
            all_steps = set()
            for s in items:
                all_steps.update(s["step"])
            common_step = np.array(sorted(all_steps))

            interpolated = []
            for s in items:
                arr_step = np.array(s["step"])
                arr_val = np.array(s["value"])
                interp_val = np.interp(common_step, arr_step, arr_val)
                interpolated.append(interp_val)

            stacked = np.stack(interpolated, axis=0)
            mean_val = np.mean(stacked, axis=0)
            min_val = np.min(stacked, axis=0)
            max_val = np.max(stacked, axis=0)

            agg = dict(items[0])  # copy first item's metadata
            agg["step"] = common_step.tolist()
            agg["value"] = mean_val.tolist()
            agg["value_min"] = min_val.tolist()
            agg["value_max"] = max_val.tolist()
            agg["aggregated"] = True
            agg["n_runs"] = len(items)
            result.append(agg)
    return result


# 最終性能を算出する末尾区間の割合（学習の最後10%）
LAST_FRACTION = 0.10


def compute_last_10k_stats(series_list):
    """Compute final-performance mean and across-seed std for each method.

    For each run (series), average the values over the last LAST_FRACTION (=10%)
    of its step span. Then report the mean of those per-run means, and the std
    ACROSS runs (seeds) — the convention used in RL/MARL papers. With a single
    run the across-seed std is undefined, so std is returned as None.
    """
    from collections import defaultdict
    groups = defaultdict(list)
    for s in series_list:
        groups[s.get("method_name", s.get("label", ""))].append(s)

    stats = []
    for method_name, items in groups.items():
        color_index = items[0].get("color_index", 0)
        method_id = items[0].get("method_id", "")
        per_run_means = []
        for s in items:
            steps = np.array(s["step"], dtype=float)
            values = np.array(s["value"], dtype=float)
            if len(steps) == 0:
                continue
            lo, hi = steps[0], steps[-1]
            threshold = hi - LAST_FRACTION * (hi - lo)
            mask = steps >= threshold
            if np.any(mask):
                per_run_means.append(float(np.mean(values[mask])))
        if per_run_means:
            mean_val = float(np.mean(per_run_means))
            # Sample std (ddof=1) across seeds; undefined for a single run.
            std_val = float(np.std(per_run_means, ddof=1)) if len(per_run_means) > 1 else None
            stats.append({
                "method_name": method_name,
                "method_id": method_id,
                "color_index": color_index,
                "mean": mean_val,
                "std": std_val,
                "n_runs": len(per_run_means)
            })
    return stats


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


@app.route("/api/method/reorder", methods=["POST"])
def reorder_methods():
    """手法の順序を更新"""
    data = request.get_json(force=True)
    sid = data.get("session_id", DEFAULT_SESSION)
    new_order = data.get("order", [])  # list of method_ids

    session = _ensure_session(sid)
    
    # 現在のメソッドをIDでマッピング
    method_map = {m["id"]: m for m in session["methods"]}
    
    # 新しい順序でリストを再構築
    reordered = []
    for mid in new_order:
        if mid in method_map:
            reordered.append(method_map[mid])
            del method_map[mid]
            
    # 指定されなかった残りのメソッドを後ろに追加（安全のため）
    reordered.extend(method_map.values())
    
    session["methods"] = reordered
    return jsonify({"ok": True})


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
    
    # 動的に現在のすべてのファイルからマップとエージェント数を収集
    current_maps = set()
    current_agents = set()
    for m in session["methods"]:
        for f in m["files"]:
            m_name = extract_map_name(f["filename"])
            a_count = extract_agent_count(f["filename"])
            if m_name: current_maps.add(m_name)
            if a_count: current_agents.add(a_count)

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

        # Check map/agents mismatches against currently existing files
        file_map = extract_map_name(filename)
        file_agents = extract_agent_count(filename)
        
        warning_msg = None
        if file_map and current_maps and file_map not in current_maps:
            warning_msg = f"マップ名が異なります (既存: {', '.join(current_maps)}, 今回: {file_map})"
        elif file_agents and current_agents and file_agents not in current_agents:
            warning_msg = f"エージェント数が異なります (既存: {', '.join(current_agents)}, 今回: {file_agents})"

        if file_map:
            current_maps.add(file_map)
            if not detected_map: detected_map = file_map
        if file_agents:
            current_agents.add(file_agents)
            if not detected_agents: detected_agents = file_agents

        target["files"].append({
            "id": file_id,
            "filename": filename,
            "metric": metric,
            "step": step,
            "value": value,
            "raw_bytes": file_bytes,
        })
        results.append({
            "file_id": file_id,
            "filename": filename,
            "metric": metric,
            "points": len(step),
            "warning": warning_msg,
        })

    # Store detected values (always update with latest detection)
    if detected_map:
        session["map_name"] = detected_map
    if detected_agents:
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


@app.route("/api/files/clear-all", methods=["POST"])
def clear_all_files():
    """全ての手法の全ファイルを削除"""
    data = request.get_json(force=True)
    sid = data.get("session_id", DEFAULT_SESSION)
    session = _ensure_session(sid)
    
    for method in session["methods"]:
        method["files"] = []
        
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
                 "timeout_rate", "cost_mean", "cost", "success_rate", "reward",
                 "episode_len", "task_completion_mean", "task_completion"]
    ordered_metrics = [m for m in preferred if m in metrics_data]
    ordered_metrics += [m for m in metrics_data if m not in ordered_metrics]

    result = []
    for metric in ordered_metrics:
        s_list = metrics_data[metric]
        stats = compute_last_10k_stats(s_list)
        result.append({
            "metric": metric,
            "y_label": get_y_label(metric),
            "series": s_list,
            "stats": stats,
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
    category = params.get("category", "")
    memo = params.get("memo", "")
    figsize_str = f"{int(fig_w)}-{int(fig_h)}"
    parts = []
    if map_name:
        parts.append(map_name)
    if agent_count:
        parts.append(f"{agent_count}agent")
    if category:
        parts.append(category)
    if memo:
        parts.append(memo)
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
    font_label = params.get("font_label", 35)
    font_tick = params.get("font_tick", 35)
    font_legend = params.get("font_legend", 43)
    method_colors = params.get("method_colors", {})
    show_grid = params.get("show_grid", True)
    show_range = params.get("show_range", True)
    legend_auto = params.get("legend_auto", True)
    legend_x = params.get("legend_x", 1.0)
    legend_y = params.get("legend_y", 1.0)
    smoothing = params.get("smoothing", 0) or 0

    rcParams["font.size"] = 18
    rcParams["axes.titlesize"] = font_label
    rcParams["axes.labelsize"] = font_label
    rcParams["xtick.labelsize"] = font_tick
    rcParams["ytick.labelsize"] = font_tick
    rcParams["legend.fontsize"] = font_legend
    rcParams["legend.title_fontsize"] = int(font_legend * 0.7)

    fig, ax = plt.subplots(1, 1, figsize=(fig_w, fig_h))
    # Apply TensorBoard-style EMA smoothing to each raw run before aggregation,
    # so that both the mean line and the min/max band reflect the smoothed curves.
    if smoothing > 0:
        for s in series_list:
            s["value"] = _smooth_ema(s["value"], smoothing)

    # Aggregate series: group by method_id, compute mean + min/max if multiple
    series_list = _aggregate_series(series_list)

    for s in series_list:
        step = s["step"]
        value = s["value"]
        value_min = s.get("value_min")
        value_max = s.get("value_max")
        if min_step is not None or max_step is not None:
            indices = [i for i, st in enumerate(step)
                       if (min_step is None or st >= min_step) and
                          (max_step is None or st <= max_step)]
            if indices:
                step = [step[i] for i in indices]
                value = [value[i] for i in indices]
                if value_min is not None:
                    value_min = [value_min[i] for i in indices]
                    value_max = [value_max[i] for i in indices]
            else:
                continue
        mid = s.get("method_id", "")
        color = method_colors.get(mid, DEFAULT_COLORS[s["color_index"] % len(DEFAULT_COLORS)])
        ax.plot(step, value, linewidth=line_width, label=s["label"], color=color)
        if show_range and s.get("aggregated") and value_min is not None and value_max is not None:
            ax.fill_between(step, value_min, value_max, alpha=0.2, color=color)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    if "rate" in y_label.lower():
        ax.set_ylim(-0.05, 1.05)
    if show_grid:
        ax.grid(True, alpha=0.3)
    if show_legend:
        if legend_auto:
            ax.legend(loc="best", framealpha=0.9)
        else:
            ax.legend(bbox_to_anchor=(legend_x, legend_y), loc="upper right", framealpha=0.9)
    plt.tight_layout()

    buf = io.BytesIO()
    save_kwargs = {"bbox_inches": "tight"}
    if fmt == "png":
        save_kwargs["dpi"] = dpi
    fig.savefig(buf, format=fmt, **save_kwargs)
    plt.close(fig)
    buf.seek(0)
    return buf


def _render_legend_to_buf(entries, params, fmt):
    """Render a standalone legend (line samples + labels only, no axes) and
    crop the output tightly to the legend box.

    entries: list of {"label": str, "color": str}
    Layout: a single row by default; wraps to 2 rows when there are many
    entries (> legend_max_per_row).
    """
    from matplotlib.lines import Line2D

    line_width = params.get("legend_line_width", params.get("line_width", 3))
    font_legend = params.get("legend_font", params.get("font_legend", 24))
    dpi = params.get("dpi", 300)
    show_frame = params.get("legend_frame", False)
    transparent = params.get("legend_transparent", True)
    orientation = params.get("legend_orientation", "horizontal")
    max_per_row = params.get("legend_max_per_row", 8)

    n = len(entries)
    if orientation == "vertical":
        ncol = 1
    else:
        ncol = params.get("legend_ncol")
        if not ncol:
            # 基本は1行、多い場合のみ2行に折り返す
            if n <= max_per_row:
                ncol = n
            else:
                ncol = -(-n // 2)  # ceil(n / 2) → 2 rows
    ncol = max(1, int(ncol))

    rcParams["legend.fontsize"] = font_legend

    # The figure size does not constrain the legend: get_window_extent()
    # reports the true rendered extent and bbox_inches crops to it. Use a
    # generous canvas so nothing is clipped before measuring.
    fig = plt.figure(figsize=(max(ncol * 3, 10), max(n / max(ncol, 1), 2.5)))
    handles = [Line2D([0], [0], color=e["color"], lw=line_width) for e in entries]
    labels = [e["label"] for e in entries]
    legend = fig.legend(handles, labels, loc="center", ncol=ncol,
                        frameon=show_frame, framealpha=0.9)

    fig.canvas.draw()
    bbox = legend.get_window_extent().transformed(fig.dpi_scale_trans.inverted())

    buf = io.BytesIO()
    save_kwargs = {"bbox_inches": bbox, "pad_inches": 0.05, "transparent": transparent}
    if fmt == "png":
        save_kwargs["dpi"] = dpi
    fig.savefig(buf, format=fmt, **save_kwargs)
    plt.close(fig)
    buf.seek(0)
    return buf


@app.route("/api/export-legend", methods=["POST"])
def export_legend():
    """手法の凡例だけを独立したファイル(PDF等)として書き出す。

    論文で複数の図を並べ、その上に共通凡例を1つ貼る用途向け。
    """
    data = request.get_json(force=True)
    sid = data.get("session_id", DEFAULT_SESSION)
    fmt = data.get("format", "pdf")
    params = data.get("params", {})
    session = _ensure_session(sid)

    method_colors = params.get("method_colors", {})
    entries = []
    for method in session["methods"]:
        if not method["files"]:
            continue  # グラフに出ない手法は凡例にも出さない
        color = method_colors.get(
            method["id"],
            DEFAULT_COLORS[method["color_index"] % len(DEFAULT_COLORS)],
        )
        entries.append({"label": method["name"], "color": color})

    if not entries:
        return jsonify({"error": "凡例に出せる手法がありません"}), 400

    buf = _render_legend_to_buf(entries, params, fmt)

    mime = {"png": "image/png", "pdf": "application/pdf",
            "eps": "application/postscript", "svg": "image/svg+xml"}
    download_name = _build_filename(params, session, "legend", fmt)
    return send_file(
        buf,
        mimetype=mime.get(fmt, "application/octet-stream"),
        as_attachment=True,
        download_name=download_name,
    )


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
    legend_settings = params.get("legend_settings", {})
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for metric, mdata in all_metrics.items():
            p = dict(params)
            p["y_label"] = mdata["y_label"]
            p["x_label"] = "Training steps"
            # Apply per-metric legend settings
            if metric in legend_settings:
                ls = legend_settings[metric]
                p["legend_auto"] = ls.get("auto", True)
                p["legend_x"] = ls.get("x", 1.0)
                p["legend_y"] = ls.get("y", 1.0)
            graph_buf = _render_graph_to_buf(mdata["series"], p, fmt)
            filename = _build_filename(params, session, metric, fmt)
            zf.writestr(filename, graph_buf.getvalue())

    zip_buf.seek(0)
    map_name = params.get("map_name", session.get("map_name", "graphs"))
    agent_count = params.get("agent_count", session.get("agent_count", ""))
    category = params.get("category", "")
    memo = params.get("memo", "")
    zip_parts = []
    if map_name:
        zip_parts.append(map_name)
    if agent_count:
        zip_parts.append(f"{agent_count}agent")
    if category:
        zip_parts.append(category)
    if memo:
        zip_parts.append(memo)
    zip_parts.append("all_metrics")
    zip_name = "_".join(zip_parts) + ".zip"

    return send_file(
        zip_buf,
        mimetype="application/zip",
        as_attachment=True,
        download_name=zip_name,
    )


@app.route("/api/export-csv", methods=["POST"])
def export_csv_zip():
    """アップロード済みCSVを手法ごとにフォルダ分けしたZIPでダウンロード"""
    data = request.get_json(force=True)
    sid = data.get("session_id", DEFAULT_SESSION)
    session = _ensure_session(sid)

    if not session["methods"]:
        return jsonify({"error": "データがありません"}), 400

    map_name = data.get("map_name", session.get("map_name", ""))
    agent_count = data.get("agent_count", session.get("agent_count", ""))
    category = data.get("category", "")
    memo = data.get("memo", "")

    # Build root folder name
    root_parts = []
    if map_name:
        root_parts.append(map_name)
    if agent_count:
        root_parts.append(f"{agent_count}agent")
    if category:
        root_parts.append(category)
    if memo:
        root_parts.append(memo)
    root_folder = "_".join(root_parts) if root_parts else "csv_data"

    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for method in session["methods"]:
            method_name = method["name"]
            for f in method["files"]:
                # Sanitize folder/file names for ZIP
                safe_method = re.sub(r'[<>:"/\\|?*]', '_', method_name)
                filename = f["filename"]
                
                # Extract run name from filename to group by execution
                name_noext = os.path.splitext(filename)[0]
                pos = name_noext.find("-tag-")
                if pos != -1:
                    run_name = name_noext[:pos]
                else:
                    run_name = name_noext
                safe_run_name = re.sub(r'[<>:"/\\|?*]', '_', run_name)
                
                path_in_zip = f"{root_folder}/{safe_method}/{safe_run_name}/{filename}"
                if "raw_bytes" in f:
                    zf.writestr(path_in_zip, f["raw_bytes"])
                else:
                    # Fallback: reconstruct CSV from step/value
                    csv_buf = io.StringIO()
                    csv_buf.write("Step,Value\n")
                    for s, v in zip(f["step"], f["value"]):
                        csv_buf.write(f"{s},{v}\n")
                    zf.writestr(path_in_zip, csv_buf.getvalue())

    zip_buf.seek(0)
    zip_name = root_folder + "_csv.zip"

    return send_file(
        zip_buf,
        mimetype="application/zip",
        as_attachment=True,
        download_name=zip_name,
    )


@app.route("/api/import-csv-zip", methods=["POST"])
def import_csv_zip():
    """CSV整理ZIPを読み込んで手法・ファイルを復元する"""
    sid = request.form.get("session_id", DEFAULT_SESSION)
    session = _ensure_session(sid)

    zip_file = request.files.get("file")
    if not zip_file:
        return jsonify({"error": "ZIPファイルが指定されていません"}), 400

    try:
        zip_bytes = zip_file.read()
        zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
    except Exception as e:
        return jsonify({"error": f"ZIPファイルの読み込みに失敗: {str(e)}"}), 400

    # Parse ZIP structure: {root_folder}/{method_name}/{run_name}/{filename.csv}
    # or {root_folder}/{method_name}/{filename.csv}
    method_files = {}  # method_name -> [{filename, file_bytes}]

    for name in zf.namelist():
        # Skip directories and non-CSV files
        if name.endswith('/') or not name.lower().endswith('.csv'):
            continue

        parts = name.split('/')
        # Determine method name from path structure
        # Expected: root/method/run/file.csv (4 parts) or root/method/file.csv (3 parts)
        if len(parts) >= 4:
            method_name = parts[1]
        elif len(parts) == 3:
            method_name = parts[1]
        elif len(parts) == 2:
            method_name = parts[0]
        else:
            method_name = "unknown"

        csv_filename = parts[-1]
        file_bytes = zf.read(name)

        if method_name not in method_files:
            method_files[method_name] = []
        method_files[method_name].append({
            "filename": csv_filename,
            "file_bytes": file_bytes,
        })

    zf.close()

    if not method_files:
        return jsonify({"error": "ZIPにCSVファイルが見つかりません"}), 400

    # Create methods and load files
    results = []
    created_methods = []
    detected_map = ""
    detected_agents = ""

    for method_name, files in method_files.items():
        # Check if method already exists
        existing = None
        for m in session["methods"]:
            if m["name"] == method_name:
                existing = m
                break

        if existing:
            target = existing
        else:
            mid = str(uuid.uuid4())[:8]
            color_index = len(session["methods"])
            target = {
                "id": mid,
                "name": method_name,
                "color_index": color_index,
                "files": [],
            }
            session["methods"].append(target)
            created_methods.append({
                "method_id": mid,
                "name": method_name,
                "color_index": color_index,
            })

        for file_info in files:
            filename = file_info["filename"]
            file_bytes = file_info["file_bytes"]
            try:
                step, value = load_csv_data(file_bytes)
            except Exception as e:
                results.append({"filename": filename, "error": str(e)})
                continue

            metric = detect_metric(filename)
            file_id = str(uuid.uuid4())[:8]

            file_map = extract_map_name(filename)
            file_agents = extract_agent_count(filename)
            if file_map and not detected_map:
                detected_map = file_map
            if file_agents and not detected_agents:
                detected_agents = file_agents

            target["files"].append({
                "id": file_id,
                "filename": filename,
                "metric": metric,
                "step": step,
                "value": value,
                "raw_bytes": file_bytes,
            })
            results.append({
                "file_id": file_id,
                "filename": filename,
                "metric": metric,
                "points": len(step),
            })

    if detected_map:
        session["map_name"] = detected_map
    if detected_agents:
        session["agent_count"] = detected_agents

    return jsonify({
        "results": results,
        "created_methods": created_methods,
        "map_name": session.get("map_name", ""),
        "agent_count": session.get("agent_count", ""),
    })


if __name__ == "__main__":
    app.run(debug=True, port=5050)
