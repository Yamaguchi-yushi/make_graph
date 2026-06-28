# Graph Visualizer — CSV Visualization Tool

A web application that creates interactive graphs from CSV files and exports them as high-quality images (PNG / PDF / EPS).

## Languages / 言語

- [English](#english)
- [日本語](#日本語)

---

## English

### Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [CSV File Naming Convention](#csv-file-naming-convention)
- [Project Structure](#project-structure)
- [License](#license)

### Features

- **Comparison of multiple methods**: Manage CSVs per method (e.g. "conventional method", "proposed method", "related work") and overlay them on a single graph
- **Automatic metric detection**: Automatically recognizes metrics such as `goal_rate` and `collision_mean` from the `-tag-XXX` pattern in file names
- **Multi-seed averaging + range display**: When multiple CSVs exist for the same method and metric, draws a **mean line** + a **min/max shaded range** (`fill_between`) in a paper-style format
- **Real-time preview**: Instantly previews high-quality Matplotlib images when parameters change
- **Batch export**: Download graphs of all metrics as a ZIP per PNG / PDF / EPS format
- **Color-vision-friendly palette**: Uses a color-vision-deficiency-friendly palette by default
- **Drag & drop upload**: Upload files intuitively via drag and drop

### Requirements

- Python 3.10+
- Dependencies: Flask, pandas, matplotlib, numpy

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd make_graph

# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py
```

Open http://localhost:5050 in your browser.

### Usage

#### Web app (`app.py`)

1. **Add a method**: Click the "＋ Add method" button in the sidebar
2. **Upload CSVs**: Drag and drop CSV files into each method's drop zone
3. **Check the graph**: A tab is automatically generated per metric and a preview is shown
4. **Adjust parameters**: Set figure size, font size, step range, legend visibility, etc.
5. **Export**: Download PNG/PDF/EPS individually, or click "Save all" to download all metrics as a single ZIP

##### Averaging across multiple-seed experiments

When you **upload multiple CSVs** with the same metric for the same method, the tool automatically:
- Draws a **mean line** (solid line)
- Shades the **min–max range** with a light color (`fill_between`)

#### CLI script (`make_multi_panel_plots.py`)

```bash
# Basic run (generates graphs from CSVs in the ./logs directory)
python make_multi_panel_plots.py

# Example options
python make_multi_panel_plots.py \
  --root ./logs \
  --out images \
  --figsize 12x8 \
  --max-step 8M \
  --save-pdf \
  --legend-suffix-order "従来手法,関連研究,提案手法"
```

**Main options:**

| Option | Description | Default |
|---|---|---|
| `--root` | Directory to scan for CSVs | `./logs` |
| `--out` | Output directory (inside `--root`) | `images` |
| `--figsize` | Figure size (`width x height`) | `10x7.5` |
| `--dpi` | PNG resolution | `300` |
| `--min-step` / `--max-step` | Step range (e.g. `1M`, `8M`) | none |
| `--save-pdf` / `--save-eps` | Also save PDF/EPS formats | `false` |
| `--no-legend` | Hide the legend | `false` |
| `--legend-suffix-order` | Legend display order | auto |
| `--filter` | File name filter (regex) | none |
| `--map` / `--agents` | Map name / agent count filter | none |

### CSV File Naming Convention

File names must follow the pattern below:

```
run-<algorithm>_seed<number>_..._map_<map-name>-v<version>_...-tag-<metric-name>_<method-label>.csv
```

Example:
```
run-qmix_seed42823329_drp_env_drp-3agent_map_8x5-v2_2025-12-02-tag-goal_mean_提案手法.csv
```

### Project Structure

```
make_graph/
├── app.py                    # Flask server (web app)
├── make_multi_panel_plots.py # CLI script
├── requirements.txt          # Dependencies
├── templates/
│   └── index.html            # UI template
├── static/
│   ├── app.js                # Frontend logic
│   └── style.css             # Stylesheet
└── logs/                     # CSV data (for the CLI script)
```

### License

MIT

---

## 日本語

CSVファイルからインタラクティブなグラフを作成し、高品質な画像（PNG / PDF / EPS）としてエクスポートするWebアプリケーションです。

### 目次

- [特徴](#特徴)
- [必要環境](#必要環境)
- [セットアップ](#セットアップ)
- [使い方](#使い方)
- [CSVファイル命名規則](#csvファイル命名規則)
- [プロジェクト構成](#プロジェクト構成)
- [ライセンス](#ライセンス)

### 特徴

- **複数手法の比較**: 「従来手法」「提案手法」「関連研究」など、手法ごとにCSVを管理してグラフに重ねて描画
- **メトリクス自動検出**: ファイル名の `-tag-XXX` パターンから `goal_rate`, `collision_mean` などのメトリクスを自動認識
- **複数seed平均＋範囲表示**: 同一手法・同一メトリクスに複数CSVがある場合、**平均線** + **min/max の塗りつぶし範囲**（`fill_between`）を論文風に描画
- **リアルタイムプレビュー**: パラメータ変更時にMatplotlibの高品質画像を即座にプレビュー
- **一括エクスポート**: 全メトリクスのグラフをPNG / PDF / EPS形式ごとにZIPで一括ダウンロード
- **色覚多様性対応カラーパレット**: デフォルトで色覚多様性に配慮した配色を使用
- **Drag & Drop アップロード**: ファイルをドラッグ＆ドロップで直感的にアップロード

### 必要環境

- Python 3.10+
- 依存パッケージ: Flask, pandas, matplotlib, numpy

### セットアップ

```bash
# リポジトリをクローン
git clone <repository-url>
cd make_graph

# 依存パッケージをインストール
pip install -r requirements.txt

# サーバーを起動
python app.py
```

ブラウザで http://localhost:5050 を開いてください。

### 使い方

#### Webアプリ (`app.py`)

1. **手法を追加**: サイドバーの「＋ 手法追加」ボタンをクリック
2. **CSVをアップロード**: 各手法のドロップゾーンにCSVファイルをドラッグ＆ドロップ
3. **グラフを確認**: メトリクスごとにタブが自動生成され、プレビューが表示
4. **パラメータを調整**: 図の大きさ、フォントサイズ、ステップ範囲、凡例の表示/非表示などを設定
5. **エクスポート**: 個別にPNG/PDF/EPSをダウンロード、または「全保存」ボタンで全メトリクスを一括ZIPダウンロード

##### 複数seed実験の平均表示

同じ手法に同じメトリクスのCSVを**複数アップロード**すると、自動的に：
- **平均線**（実線）を描画
- **min〜maxの範囲**を薄い色で塗りつぶし（`fill_between`）

#### CLIスクリプト (`make_multi_panel_plots.py`)

```bash
# 基本実行（./logs ディレクトリのCSVからグラフ生成）
python make_multi_panel_plots.py

# オプション例
python make_multi_panel_plots.py \
  --root ./logs \
  --out images \
  --figsize 12x8 \
  --max-step 8M \
  --save-pdf \
  --legend-suffix-order "従来手法,関連研究,提案手法"
```

**主なオプション:**

| オプション | 説明 | デフォルト |
|---|---|---|
| `--root` | CSVスキャンディレクトリ | `./logs` |
| `--out` | 出力ディレクトリ（`--root`内） | `images` |
| `--figsize` | 図サイズ（`幅x高さ`） | `10x7.5` |
| `--dpi` | PNG解像度 | `300` |
| `--min-step` / `--max-step` | ステップ範囲（例: `1M`, `8M`） | なし |
| `--save-pdf` / `--save-eps` | PDF/EPS形式も保存 | `false` |
| `--no-legend` | 凡例を非表示 | `false` |
| `--legend-suffix-order` | 凡例の表示順序 | 自動 |
| `--filter` | ファイル名フィルタ（正規表現） | なし |
| `--map` / `--agents` | マップ名・エージェント数フィルタ | なし |

### CSVファイル命名規則

ファイル名は以下のパターンに従う必要があります:

```
run-<アルゴリズム>_seed<数値>_..._map_<マップ名>-v<バージョン>_...-tag-<メトリクス名>_<手法ラベル>.csv
```

例:
```
run-qmix_seed42823329_drp_env_drp-3agent_map_8x5-v2_2025-12-02-tag-goal_mean_提案手法.csv
```

### プロジェクト構成

```
make_graph/
├── app.py                    # Flaskサーバー（Webアプリ）
├── make_multi_panel_plots.py # CLIスクリプト
├── requirements.txt          # 依存パッケージ
├── templates/
│   └── index.html            # UIテンプレート
├── static/
│   ├── app.js                # フロントエンドロジック
│   └── style.css             # スタイルシート
└── logs/                     # CSVデータ（CLIスクリプト用）
```

### ライセンス

MIT
