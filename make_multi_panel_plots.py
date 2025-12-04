# make_multi_panel_plots.py
# CSV only / PNG save / no titles / English axes
# Legend default: "{method}（{category}）"
# NEW: --legend-method-order / --legend-category-order to control legend order.

import argparse, os, re, glob, json
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams

# Japanese font fallback (optional)
for _name in ["Hiragino Sans", "Noto Sans CJK JP", "Yu Gothic", "IPAexGothic"]:
    if any(_name in f.name for f in font_manager.fontManager.ttflist):
        rcParams["font.family"] = _name
        break
rcParams["axes.unicode_minus"] = False
rcParams["pdf.fonttype"] = 42
rcParams["ps.fonttype"]  = 42

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
    category: Optional[str]
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
    return dict(metric=metric, method=method, category=category, basename=base)

def build_label(meta: Dict[str, Optional[str]], template: Optional[str]) -> str:
    data = {"method": meta.get("method") or "", "category": meta.get("category") or "",
            "metric": meta.get("metric") or "", "basename": meta.get("basename") or ""}
    tmpl = template or "{category}"
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

def sort_series(series: List[SeriesMeta], method_order: Optional[List[str]], cat_order: Optional[List[str]]):
    mrank = {m:i for i,m in enumerate(method_order)} if method_order else {}
    crank = {c:i for i,c in enumerate(cat_order)} if cat_order else {}
    def key(s: SeriesMeta):
        return (mrank.get(s.method, 10**9), crank.get(s.category, 10**9),
                s.method or "", s.category or "", s.src)
    return sorted(series, key=key)

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
    ap.add_argument("--oneplot", default=None, help="Metric to overlay on a single axes")
    ap.add_argument("--filter", default=None, help="Regex to filter basenames")
    ap.add_argument("--map", default=None, help="Filter by map name (e.g., '8x5-v2')")
    ap.add_argument("--agents", default=None, help="Filter by agent count (e.g., '3')")
    ap.add_argument("--method-map", default=None, help="Map filename REGEX to method label")
    ap.add_argument("--category-map", default=None, help="Map filename REGEX to category label")
    ap.add_argument("--label-template", default=None, help='Legend template (default "{category}")')
    ap.add_argument("--legend-method-order", default=None, help='Comma list e.g. "IQL,QMIX"')
    ap.add_argument("--legend-category-order", default="従来手法,関連研究,提案手法", help='Comma list; default "従来手法,関連研究,提案手法"')
    ap.add_argument("--save-pdf", action="store_true", help="Also save PDF")
    ap.add_argument("--max-step", type=str, default=None, help="Max step to display (e.g., '8M', '5000000', '2.5M')")
    ap.add_argument("--min-step", type=str, default=None, help="Min step to display (e.g., '1M', '100000')")
    args = ap.parse_args()

    # 出力ディレクトリを作成
    output_dir = os.path.join(args.root, args.out)
    os.makedirs(output_dir, exist_ok=True)

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
    category_rules = parse_mapping(args.category_map)
    method_order = parse_order_list(args.legend_method_order)
    category_order = parse_order_list(args.legend_category_order) or ["従来手法", "関連研究", "提案手法"]

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
            meta["category"] = apply_map(category_rules, meta["basename"], meta.get("category"))
            label = build_label(meta, args.label_template)
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
            all_series.append(SeriesMeta(meta["metric"], step, value, meta["method"], meta["category"], label, os.path.basename(p)))

        by_metric: Dict[str, List[SeriesMeta]] = {}
        for s in all_series:
            by_metric.setdefault(s.metric, []).append(s)

        preferred = ["collision_mean", "goal_rate", "timeout_rate", "cost", "success_rate", "reward", "episode_len"]
        metrics = [m for m in preferred if m in by_metric]
        if len(metrics) < 4:
            metrics += [m for m in by_metric if m not in metrics]
        metrics = metrics[:max(1, min(4, len(metrics)))]

        for metric in metrics:  # 各メトリクスごとに画像を生成
            n = 1  # 各メトリクスは1つの画像に
            nrows, ncols = 1, 1  # 1行1列のプロット
            fig, ax = plt.subplots(nrows, ncols, figsize=(10, 7.5))

            series = sort_series(by_metric[metric], method_order, category_order)
            colors = ["blue", "red", "orange", "purple"]  # 色のリストを定義
            for i, s in enumerate(series):
                color = colors[i % len(colors)]  # 色を順番に適用
                ax.plot(s.step, s.value, linewidth=1.2, label=s.label, color=color)
            ax.set_xlabel("Training steps")
            if "rate" in metric or "ratio" in metric or "mean" in metric:
                ax.set_ylabel("Rate")
            elif "cost" in metric:
                ax.set_ylabel("Cost")
            else:
                ax.set_ylabel("Value")
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=20, loc="best", framealpha=0.9)

            plt.tight_layout()
            out_png = os.path.join(output_dir, f"{map_name}_{agent_count}agent_{metric}.png")
            fig.savefig(out_png, dpi=args.dpi, bbox_inches="tight")
            print(f"Saved: {out_png}")
            if args.save_pdf:
                out_pdf = os.path.join(output_dir, f"{map_name}_{agent_count}agent_{metric}.pdf")
                fig.savefig(out_pdf, bbox_inches="tight")
                print(f"Saved: {out_pdf}")
            plt.close(fig)

if __name__ == "__main__":
    main()
