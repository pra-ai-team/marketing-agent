## 汎用マーケティング企画・制作エージェント

業界横断で使える、マーケティング戦略立案からランディングページ制作までを支援するシンプルなツールセットです。

### 必要条件
- Windows 10/11
- Python 3.8 以上
- Cursor エディタ
- （任意）SerpAPI キー

### セットアップ
```bash
cd marketing-agent
pip install -r requirements.txt
```

### 使い方（推奨：ユーザー入力シート）
1. ルート直下の `user_input.md` を開き、「ここに入力」の行を埋める（企業名／地域は必須）
2. 実行
   ```bash
   python src/run.py --quick --force
   # または
   python src/workflows/setup-project.py --quick --force
   ```
   - 実行時に `user_input.md` の内容が `input/project-config.yaml` に自動反映されます
   - 反映をスキップしたい場合は `--no-user-input`
3. 出力確認
   - `marketing-agent/output/YYYYMMDD/` にテンプレートとナレッジが生成
   - 例: `01_competitor-analysis.md`, `02_seo-analysis.md`, `knowledge/company-info.md`

### 使い方（最短：会社名のみ）
どちらか一方だけでOK。
- ファイル方式: `input/company-name.txt` を作成して会社名を1行で記入
- 引数方式: `--company "株式会社サンプル"`

```bash
python src/run.py --quick --force
# または
python src/workflows/setup-project.py --quick --force --company "株式会社サンプル"
```

### 使い方（従来）
```bash
# 設定確認
python src/workflows/config_loader.py

# プロジェクト作成
python src/workflows/setup-project.py
# または（後方互換）
python src/workflows/generic-setup-project.py
```
Cursor で `main_prompt.md` を実行すると、戦略立案から LP 制作までの自動連鎖手順をガイドします。

### 主なオプション
- `--date YYYYMMDD`: 出力日付を指定（例: `--date 20250625`）
- `--config PATH`: 設定ファイルを指定（既定: `input/project-config.yaml`）
- `--outdir PATH`: 出力ディレクトリのベースを指定（既定: `output`）
- `--force`: 既存ディレクトリがあっても確認無しで続行
- `--quick`: 不足設定（業界・地域など）を警告化して実行
- `--company`, `--company-file`: 企業名を直接指定
- `--no-user-input`: `user_input.md` の反映をスキップ
- `--no-competitors`, `--max-competitors`, `--fetch-timeout`: 競合サイト収集制御
- `--no-inject`: 04要件定義への競合ガイド自動注入をスキップ

### ディレクトリ構成（概要）
```
marketing-agent/
├── user_input.md                  # 入力フォーム（AIが解析し config に反映）
├── input/                         # 入力（company-name.txt / project-config.yaml）
├── src/
│   ├── run.py                     # 実行ラッパー（--outdir 既定付与）
│   └── workflows/
│       ├── setup-project.py       # メインフロー/CLI
│       ├── config_loader.py       # 設定読み込み・検証・知識生成
│       ├── user_input_parser.py   # user_input.md を解析し YAML に反映
│       ├── check-progress.py      # 進捗確認
│       ├── check-system-date.py   # システム日付の診断
│       └── fix-date-mismatch.py   # 日付不一致の修正
├── src/templates/generic/         # 01〜05のテンプレートMD
├── output/YYYYMMDD/
│   ├── 01_competitor-analysis.md
│   ├── 02_seo-analysis.md
│   ├── 03_marketing-strategy.md
│   ├── 04_lp-requirements.md
│   ├── 05_lp-completion-report.md
│   ├── knowledge/company-info.md
│   └── competitors/summary.md     # 競合サイト収集レポート（自動生成）
└── docs/                          # ドキュメント/プロンプト
```

### トラブルシューティング（簡易）
- `user_input.md` が反映されない: `--no-user-input` を付けていないか確認
- 設定エラー: `python src/workflows/config_loader.py` で必須（company.name / location）を確認
- 競合収集が動かない: URL未設定時はスキップされます（警告のみ）
- SerpAPI を使う場合: Windows では `setx SERPAPI_KEY your_api_key` を設定
 - システム日付が不正で日付ディレクトリと内容がズレる: `python src/workflows/check-system-date.py` で診断し、必要に応じて `python src/workflows/fix-date-mismatch.py --method update_files --yes` を実行
 - 進捗を一覧で確認したい: `python src/workflows/check-progress.py`

---
最終更新: 2025-08-08 / バージョン: v3.2