# make_multi_panel_plots.py
# CSV only / PNG save / no titles / English axes
# Legend default: "{method}（{category}）"
# NEW: --legend-method-order / --legend-category-order to control legend order.

import argparse, os, re, glob, json
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional

import pandas as pd
import matplotlib
matplotlib.use("module://matplotlib.backends.backend_cairo")
import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams

# Japanese font fallback (optional) - より強力なフォント設定
_font_found = False
for _name in ["Hiragino Sans", "Hiragino Kaku Gothic Pro", "Noto Sans CJK JP", "Yu Gothic", "IPAexGothic", "TakaoPGothic"]:
    if any(_name in f.name for f in font_manager.fontManager.ttflist):
        rcParams["font.family"] = _name
        _font_found = True
        print(f"Using font: {_name}")
        break

# フォントが見つからない場合のフォールバック
if not _font_found:
    # システムにインストールされている日本語フォントを探す
    jp_fonts = [f for f in font_manager.fontManager.ttflist 
                if any(name in f.name for name in ['Gothic', 'Hiragino', 'Noto', 'IPA', 'Takao', 'Meiryo'])]
    if jp_fonts:
        rcParams["font.family"] = jp_fonts[0].name
        print(f"Using fallback font: {jp_fonts[0].name}")

rcParams["axes.unicode_minus"] = False

# PDF/PS用のフォント設定（Type 3 = フォントをアウトライン化）
rcParams["pdf.fonttype"] = 3
rcParams["ps.fonttype"]  = 3

# グローバルフォントサイズ設定（軸ラベルを大きく）
rcParams["font.size"] = 18           # 基本フォントサイズ
rcParams["axes.titlesize"] = 24      # タイトル
rcParams["axes.labelsize"] = 30      # 軸ラベル（大きく）
rcParams["xtick.labelsize"] = 25     # x軸目盛り
rcParams["ytick.labelsize"] = 25     # y軸目盛り
rcParams["legend.fontsize"] = 30     # 凡例（ここで設定）
rcParams["legend.title_fontsize"] = 20  # 凡例タイトル

CANONICAL = {
    "qmix":"QMIX","vdn":"VDN","iql":"IQL","dqn":"DQN",
    "ppo":"PPO","mappo":"MAPPO","ippo":"IPPO","coma":"COMA",
    "sac":"SAC","td3":"TD3","ddpg":"DDPG","maddpg":"MADDPG",
    "drp":"DRP"
}
IGNORE_TOKENS = {"drp_env","env","map","agent","agents","seed","tag","run","train","test","eval","v1","v2","v3","v4"}

def _normalize(name: str) -> str:
    key = name.lower()
    return CANONICAL.get(key, name.upper())

def detect_method_label(csv_path: str) -> Optional[str]:
    base = os.path.basename(csv_path); stem, _ = os.path.splitext(csv_path)
    # sidecar .method/.txt
    for ext in (".method",".txt"):
        p = stem+ext
        if os.path.exists(p):
            line = open(p,encoding="utf-8").readline().strip()
            if line: return _normalize(line)
    # sidecar json
    for ext in (".json",".meta.json",".hparams.json"):
        p = stem+ext
        if os.path.exists(p):
            try:
                obj = json.load(open(p,"r",encoding="utf-8"))
                for k in ("method","algo","algorithm","agent","name","run_name"):
                    v = obj.get(k)
                    if isinstance(v,str) and v.strip(): return _normalize(v.strip())
            except Exception: pass
    # sidecar yaml/yml (light parse)
    for ext in (".yaml",".yml"):
        p = stem+ext
        if os.path.exists(p):
            try:
                for line in open(p,"r",encoding="utf-8"):
                    m = re.match(r"\s*(method|algo|algorithm)\s*:\s*([^\s#]+)", line)
                    if m: return _normalize(m.group(2))
            except Exception: pass
    # CSV columns (constant)
    try:
        df = pd.read_csv(csv_path, nrows=200)
        for col in df.columns:
            if col.lower() in ("method","algo","algorithm","agent","run","run_name","experiment"):
                vals = [str(v) for v in df[col].dropna().unique().tolist()]
                if len(vals)==1: return _normalize(vals[0])
    except Exception: pass
    # tokens
    tokens = re.split(r"[_\-.]+", os.path.splitext(base)[0])
    for t in tokens:
        if not t or t.isdigit(): continue
        tl = t.lower()
        if tl in IGNORE_TOKENS: continue
        if tl in CANONICAL: return CANONICAL[tl]
    # run-<algo>_
    m = re.search(r"run-([A-Za-z0-9]+)_", base)
    if m: return _normalize(m.group(1))
    # dirs
    parts = [p.lower() for p in re.split(r"[\\/]+", os.path.dirname(csv_path)) if p]
    for p in reversed(parts):
        if p in CANONICAL: return CANONICAL[p]
    return None

@dataclass
class SeriesMeta:
    metric: str
    step: List[float]
    value: List[float]
    method: Optional[str]
    suffix: Optional[str]  # category から suffix に変更
    label: str
    src: str

def parse_mapping(s: Optional[str]):
    if not s: return []
    parts = [p.strip() for p in re.split(r'[;]', s) if p.strip()]
    out = []
    for p in parts:
        if '=' in p:
            k,v = p.split('=',1)
            out.append((re.compile(k.strip(), re.IGNORECASE), v.strip()))
        else:
            out.append((re.compile(p.strip(), re.IGNORECASE), p.strip()))
    return out

def extract_suffix(name_noext: str) -> str:
    """ファイル名の.csv直前の最後の_以降の文字列を抽出
    
    例: 
    - "run-qmix_...-tag-collision_mean_関連研究" -> "関連研究"
    - "run-qmix_...-tag-goal_rate_提案手法" -> "提案手法"
    - "run-qmix_...-tag-collision_mean_二段階学習" -> "二段階学習"
    """
    # 最後の_以降を取得
    last_underscore = name_noext.rfind("_")
    if last_underscore != -1 and last_underscore < len(name_noext) - 1:
        return name_noext[last_underscore + 1:]
    return name_noext  # _がない場合は全体を返す

def parse_filename(fname: str) -> Dict[str, Optional[str]]:
    base = os.path.basename(fname)
    name_noext, _ = os.path.splitext(base)

    # metric after "-tag-"
    metric = "unknown"
    pos = name_noext.find("-tag-")
    if pos != -1:
        rest = name_noext[pos + len("-tag-"):]
        m = re.match(r"([A-Za-z0-9_]+)", rest)
        if m:
            metric = m.group(1).rstrip("_")

    # suffix: 最後の_以降の文字列を抽出
    suffix = extract_suffix(name_noext)

    # category from Japanese tokens (suffix preferred)
    category = None
    if re.search(r"(提案手法①|提案手法②)\s*$", name_noext):
        category = re.search(r"(提案手法①|提案手法②)\s*$", name_noext).group(1)
    elif re.search(r"(提案手法|提案)\s*$", name_noext):
        category = "提案手法"
    elif re.search(r"(従来手法|従来)\s*$", name_noext):
        category = "従来手法"
    elif re.search(r"(関連研究)\s*$", name_noext):
        category = "関連研究"

    if category is None:
        if re.search(r"(提案手法①|提案手法②)", name_noext):
            category = re.search(r"(提案手法①|提案手法②)", name_noext).group(1)
        elif re.search(r"(提案手法|提案)", name_noext):
            category = "提案手法"
        elif re.search(r"(従来手法|従来)", name_noext):
            category = "従来手法"
        elif re.search(r"(関連研究)", name_noext):
            category = "関連研究"

    method = detect_method_label(fname)
    return dict(metric=metric, method=method, category=category, suffix=suffix, basename=base)

def build_label(meta: Dict[str, Optional[str]], template: Optional[str]) -> str:
    data = {"method": meta.get("method") or "", 
            "category": meta.get("category") or "",
            "metric": meta.get("metric") or "", 
            "suffix": meta.get("suffix") or "",
            "basename": meta.get("basename") or ""}
    tmpl = template or "{suffix}"  # デフォルトをsuffixに変更
    try:
        lab = tmpl.format_map(data).strip(" 、,")
        return lab if lab else meta.get("basename", "")
    except Exception:
        return meta.get("basename", "")

def load_csv(path: str):
    df = pd.read_csv(path)
    cols = [c.lower() for c in df.columns]
    step_col = next((df.columns[i] for i,c in enumerate(cols) if c in ["step","steps","global_step","t","x"]), None)
    if step_col is None: step_col = df.columns[1] if df.shape[1]>=2 else df.columns[0]
    value_col = next((df.columns[i] for i,c in enumerate(cols) if c in ["value","mean","y","score","metric"]), None)
    if value_col is None: value_col = df.columns[-1]
    return df[step_col].tolist(), df[value_col].tolist()

def parse_order_list(s: Optional[str]) -> Optional[List[str]]:
    if not s: return None
    return [x.strip() for x in s.split(",") if x.strip()]

def parse_step_value(s: Optional[str]) -> Optional[float]:
    """ステップ数の文字列を数値に変換 (例: '8M' -> 8000000, '2.5M' -> 2500000)"""
    if not s:
        return None
    s = s.strip().upper()
    multipliers = {'K': 1e3, 'M': 1e6, 'B': 1e9}
    for suffix, mult in multipliers.items():
        if s.endswith(suffix):
            try:
                return float(s[:-1]) * mult
            except ValueError:
                return None
    try:
        return float(s)
    except ValueError:
        return None

def parse_figsize(s: Optional[str]) -> Tuple[float, float]:
    """figsize文字列をパース (例: '10x7.5', '12,8', '16:9')"""
    if not s:
        return (10, 7.5)  # デフォルト
    # 区切り文字: x, X, ,, :
    for sep in ['x', 'X', ',', ':']:
        if sep in s:
            parts = s.split(sep)
            if len(parts) == 2:
                try:
                    return (float(parts[0].strip()), float(parts[1].strip()))
                except ValueError:
                    pass
    return (10, 7.5)  # パース失敗時のデフォルト

def filter_by_step_range(step: List[float], value: List[float], min_step: Optional[float], max_step: Optional[float]) -> Tuple[List[float], List[float]]:
    """ステップ数の範囲でデータをフィルタリング"""
    if min_step is None and max_step is None:
        return step, value
    
    filtered_step = []
    filtered_value = []
    for s, v in zip(step, value):
        if min_step is not None and s < min_step:
            continue
        if max_step is not None and s > max_step:
            continue
        filtered_step.append(s)
        filtered_value.append(v)
    
    return filtered_step, filtered_value

def sort_series(series: List[SeriesMeta], method_order: Optional[List[str]], suffix_order: Optional[List[str]]):
    mrank = {m:i for i,m in enumerate(method_order)} if method_order else {}
    srank = {s:i for i,s in enumerate(suffix_order)} if suffix_order else {}
    def key(s: SeriesMeta):
        # suffixで並び替え
        return (mrank.get(s.method, 10**9), srank.get(s.suffix, 10**9),
                s.method or "", s.suffix or "", s.src)
    return sorted(series, key=key)


def aggregate_series_for_plot(series: List[SeriesMeta]) -> List[dict]:
    """同じlabelを持つ複数のSeriesMetaを集約し、平均+min/max rangeを計算する。

    1本だけのlabelはそのまま返す。複数あるlabelは共通step軸に補間して
    mean/min/maxを計算する。戻り値はdictのリスト。
    """
    from collections import defaultdict
    groups = defaultdict(list)
    for s in series:
        groups[s.label].append(s)

    result = []
    for label, items in groups.items():
        if len(items) == 1:
            result.append({
                "step": items[0].step,
                "value": items[0].value,
                "label": items[0].label,
                "aggregated": False,
            })
        else:
            # 全seriesのstep範囲のunionを作り、共通step軸に補間
            all_steps = set()
            for s in items:
                all_steps.update(s.step)
            common_step = np.array(sorted(all_steps))

            interpolated = []
            for s in items:
                arr_step = np.array(s.step)
                arr_val = np.array(s.value)
                interp_val = np.interp(common_step, arr_step, arr_val)
                interpolated.append(interp_val)

            stacked = np.stack(interpolated, axis=0)
            mean_val = np.mean(stacked, axis=0)
            min_val = np.min(stacked, axis=0)
            max_val = np.max(stacked, axis=0)

            result.append({
                "step": common_step.tolist(),
                "value": mean_val.tolist(),
                "value_min": min_val.tolist(),
                "value_max": max_val.tolist(),
                "label": label,
                "aggregated": True,
                "n_runs": len(items),
            })
    return result

def extract_map_name(basename: str) -> str:
    # Extract map name from the basename (exclude date part)
    m = re.search(r"map_([a-zA-Z0-9xX]+)-v\d+", basename)
    return m.group(1) + "-v" + re.search(r"-v(\d+)", basename).group(1) if m else "unknown"

def extract_agent_count(basename: str) -> str:
    # Extract agent count from the basename
    m = re.search(r"(\d+)agent", basename)
    return m.group(1) if m else "unknown"

def apply_map(rules, basename, default=None):
    """正規表現ルールを適用して値をマッピング"""
    for rx, v in rules:
        if rx.search(basename):
            return v
    return default

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./logs", help="Directory to scan for *-tag-*.csv (default: ./logs)")
    ap.add_argument("--out", default="images", help="Output directory under --root (default: images)")
    ap.add_argument("--dpi", type=int, default=300, help="PNG DPI")
    ap.add_argument("--figsize", default="10x7.5", help="Figure size as 'WIDTHxHEIGHT' (e.g., '10x7.5', '12x6', '16x9')")
    ap.add_argument("--oneplot", default=None, help="Metric to overlay on a single axes")
    ap.add_argument("--filter", default=None, help="Regex to filter basenames")
    ap.add_argument("--map", default=None, help="Filter by map name (e.g., '8x5-v2')")
    ap.add_argument("--agents", default=None, help="Filter by agent count (e.g., '3')")
    ap.add_argument("--method-map", default=None, help="Map filename REGEX to method label")
    ap.add_argument("--category-map", default=None, help="Map filename REGEX to category label")
    ap.add_argument("--label-template", default=None, help='Legend template (default "{suffix}"). Available: {suffix}, {category}, {method}, {metric}, {basename}')
    ap.add_argument("--legend-method-order", default=None, help='Comma list e.g. "IQL,QMIX"')
    ap.add_argument("--legend-suffix-order", default=None, help='Comma list e.g. "従来手法,関連研究,提案手法,二段階学習"')
    ap.add_argument("--legend-category-order", default=None, help='Alias for --legend-suffix-order')  # エイリアスとして追加
    ap.add_argument("--save-pdf", action="store_true", help="Also save PDF")
    ap.add_argument("--save-eps", action="store_true", help="Also save EPS")
    ap.add_argument("--no-legend", action="store_true", help="Hide legend")
    ap.add_argument("--max-step", type=str, default=None, help="Max step to display (e.g., '8M', '5000000', '2.5M')")
    ap.add_argument("--min-step", type=str, default=None, help="Min step to display (e.g., '1M', '100000')")
    args = ap.parse_args()

    # 出力ディレクトリを作成
    output_dir = os.path.join(args.root, args.out)
    os.makedirs(output_dir, exist_ok=True)

    # figsizeのパース
    figsize = parse_figsize(args.figsize)
    print(f"Figure size: {figsize[0]} x {figsize[1]}")

    # ステップ範囲のパース
    max_step = parse_step_value(args.max_step)
    min_step = parse_step_value(args.min_step)
    if max_step:
        print(f"Max step limit: {max_step:,.0f}")
    if min_step:
        print(f"Min step limit: {min_step:,.0f}")

    # collect CSVs
    paths = []
    for pat in ["*-tag-*.csv", "*-tag-*.CSV"]:
        paths += glob.glob(os.path.join(args.root, pat))
    if args.filter:
        rx = re.compile(args.filter)
        paths = [p for p in paths if rx.search(os.path.basename(p))]
    if not paths:
        print(f"No CSV files found under {args.root}")
        return

    # メトリクスフィルタリング
    if args.oneplot:
        paths = [p for p in paths if f"-tag-{args.oneplot}" in os.path.basename(p)]
        if not paths:
            print(f"No files found for metric '{args.oneplot}'")
            return

    method_rules = parse_mapping(args.method_map)
    method_order = parse_order_list(args.legend_method_order)
    
    # legend-category-order が指定された場合も suffix_order として扱う
    suffix_order_str = args.legend_suffix_order or args.legend_category_order
    suffix_order = parse_order_list(suffix_order_str)

    # マップ名とエージェント数でグループ化
    map_groups: Dict[Tuple[str, str], List[str]] = {}
    for path in paths:
        basename = os.path.basename(path)
        map_name = extract_map_name(basename)
        agent_count = extract_agent_count(basename)
        
        # デバッグ出力
        print(f"File: {basename}")
        print(f"  Extracted map: {map_name}, agents: {agent_count}")
        print(f"  Filter map: {args.map}, filter agents: {args.agents}")
        
        # フィルタリング
        if args.map and map_name != args.map:
            print(f"  Skipped: map mismatch")
            continue
        if args.agents and agent_count != args.agents:
            print(f"  Skipped: agent count mismatch")
            continue
        
        print(f"  Added to group")
        key = (map_name, agent_count)
        map_groups.setdefault(key, []).append(path)
    
    if not map_groups:
        print(f"No files found matching the specified filters")
        return

    # 各マップ・エージェント数ごとにグラフを生成
    for (map_name, agent_count), map_paths in map_groups.items():
        print(f"Processing map: {map_name}, agents: {agent_count}")
        all_series: List[SeriesMeta] = []
        for p in map_paths:
            meta = parse_filename(p)
            meta["method"] = apply_map(method_rules, meta["basename"], meta.get("method"))
            # suffixを使用（categoryではなく）
            label = build_label(meta, args.label_template)
            print(f"  Label for {os.path.basename(p)}: '{label}' (suffix: '{meta.get('suffix')}')")
            try:
                step, value = load_csv(p)
                # ステップ範囲でフィルタリング
                step, value = filter_by_step_range(step, value, min_step, max_step)
                if not step:  # フィルタリング後にデータがない場合はスキップ
                    print(f"Skip {os.path.basename(p)}: No data in step range")
                    continue
            except Exception as e:
                print(f"Skip {os.path.basename(p)}: {e}")
                continue
            # SeriesMetaにsuffixを渡す（categoryの代わり）
            all_series.append(SeriesMeta(meta["metric"], step, value, meta["method"], meta.get("suffix"), label, os.path.basename(p)))

        by_metric: Dict[str, List[SeriesMeta]] = {}
        for s in all_series:
            by_metric.setdefault(s.metric, []).append(s)

        preferred = ["collision_mean", "goal_rate", "timeout_rate", "cost", "success_rate", "reward", "episode_len"]
        metrics = [m for m in preferred if m in by_metric]
        if len(metrics) < 4:
            metrics += [m for m in by_metric if m not in metrics]
        metrics = metrics[:max(1, min(4, len(metrics)))]

        for metric in metrics:  # 各メトリクスごとに画像を生成
            nrows, ncols = 1, 1  # 1行1列のプロット
            fig, ax = plt.subplots(nrows, ncols, figsize=figsize)

            series = sort_series(by_metric[metric], method_order, suffix_order)
            agg_series = aggregate_series_for_plot(series)
            colors = ["#03AF7A", "#005AFF", "red", "#4DC4FF", "#F6AA00", "#FFF100"]  # 色覚多様性対応
            for i, s in enumerate(agg_series):
                color = colors[i % len(colors)]  # 色を順番に適用
                ax.plot(s["step"], s["value"], linewidth=1.2, label=s["label"], color=color)
                if s.get("aggregated") and "value_min" in s and "value_max" in s:
                    ax.fill_between(s["step"], s["value_min"], s["value_max"], alpha=0.2, color=color)
            ax.set_xlabel("Training steps")
            
            # メトリクス名から縦軸ラベルを設定
            metric_lower = metric.lower()
            if "goal" in metric_lower:
                ax.set_ylabel("Goal rate")
            elif "collision" in metric_lower:
                ax.set_ylabel("Collision rate")
            elif "timeup" in metric_lower or "timeout" in metric_lower:
                ax.set_ylabel("Timeup rate")
            elif "success" in metric_lower:
                ax.set_ylabel("Success rate")
            elif "step" in metric_lower or "episode_len" in metric_lower:
                ax.set_ylabel("Episode length")
            elif "reward" in metric_lower:
                ax.set_ylabel("Reward")
            elif "cost" in metric_lower:
                ax.set_ylabel("Cost")
            elif "rate" in metric_lower or "ratio" in metric_lower:
                ax.set_ylabel("Rate")
            else:
                ax.set_ylabel("Value")
            
            ax.grid(True, alpha=0.3)
            if not args.no_legend:
                ax.legend(loc="best", framealpha=0.9)  # rcParams["legend.fontsize"]を使用

            plt.tight_layout()

            figsize_str = f"{int(figsize[0])}-{int(figsize[1])}"

            # PNG（必要なら残す）
            out_png = os.path.join(output_dir, f"{map_name}_{agent_count}agent_{metric}_{figsize_str}.png")
            fig.savefig(out_png, dpi=args.dpi, bbox_inches="tight")
            print(f"Saved: {out_png}")

            # PDF（ベクターで直接保存：ここが重要）
            if args.save_pdf:
                out_pdf = os.path.join(output_dir, f"{map_name}_{agent_count}agent_{metric}_{figsize_str}.pdf")
                fig.savefig(out_pdf, format="pdf", bbox_inches="tight")
                print(f"Saved: {out_pdf}")

            # EPS（従来どおり）
            if args.save_eps:
                out_eps = os.path.join(output_dir, f"{map_name}_{agent_count}agent_{metric}_{figsize_str}.eps")
                fig.savefig(out_eps, format="eps", bbox_inches="tight")
                print(f"Saved: {out_eps}")

            plt.close(fig)


if __name__ == "__main__":
    main()
