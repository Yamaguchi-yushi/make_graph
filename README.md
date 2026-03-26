# Graph Visualizer — CSV可視化ツール

CSVファイルからインタラクティブなグラフを作成し、高品質な画像（PNG / PDF / EPS）としてエクスポートするWebアプリケーションです。

## 特徴

- **複数手法の比較**: 「従来手法」「提案手法」「関連研究」など、手法ごとにCSVを管理してグラフに重ねて描画
- **メトリクス自動検出**: ファイル名の `-tag-XXX` パターンから `goal_rate`, `collision_mean` などのメトリクスを自動認識
- **複数seed平均＋範囲表示**: 同一手法・同一メトリクスに複数CSVがある場合、**平均線** + **min/max の塗りつぶし範囲**（`fill_between`）を論文風に描画
- **リアルタイムプレビュー**: パラメータ変更時にMatplotlibの高品質画像を即座にプレビュー
- **一括エクスポート**: 全メトリクスのグラフをPNG / PDF / EPS形式ごとにZIPで一括ダウンロード
- **色覚多様性対応カラーパレット**: デフォルトで色覚多様性に配慮した配色を使用
- **Drag & Drop アップロード**: ファイルをドラッグ＆ドロップで直感的にアップロード

## 必要環境

- Python 3.10+
- 依存パッケージ: Flask, pandas, matplotlib, numpy

## セットアップ

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

## 使い方

### Webアプリ (`app.py`)

1. **手法を追加**: サイドバーの「＋ 手法追加」ボタンをクリック
2. **CSVをアップロード**: 各手法のドロップゾーンにCSVファイルをドラッグ＆ドロップ
3. **グラフを確認**: メトリクスごとにタブが自動生成され、プレビューが表示
4. **パラメータを調整**: 図の大きさ、フォントサイズ、ステップ範囲、凡例の表示/非表示などを設定
5. **エクスポート**: 個別にPNG/PDF/EPSをダウンロード、または「全保存」ボタンで全メトリクスを一括ZIPダウンロード

#### 複数seed実験の平均表示

同じ手法に同じメトリクスのCSVを**複数アップロード**すると、自動的に：
- **平均線**（実線）を描画
- **min〜maxの範囲**を薄い色で塗りつぶし（`fill_between`）

### CLIスクリプト (`make_multi_panel_plots.py`)

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

## CSVファイル命名規則

ファイル名は以下のパターンに従う必要があります:

```
run-<アルゴリズム>_seed<数値>_..._map_<マップ名>-v<バージョン>_...-tag-<メトリクス名>_<手法ラベル>.csv
```

例:
```
run-qmix_seed42823329_drp_env_drp-3agent_map_8x5-v2_2025-12-02-tag-goal_mean_提案手法.csv
```

## プロジェクト構成

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

## ライセンス

MIT
