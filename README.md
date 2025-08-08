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

# （任意）従来設定ファイルを使う場合のみ
# PowerShell / cmd
copy input\project-config.yaml.template input\project-config.yaml
# Git Bash
cp input/project-config.yaml.template input/project-config.yaml
```

### 使い方（最短・3ステップ：シンプル構成）
1. 企業名をファイルに1行で入力
   - `marketing-agent/input/company-name.txt` を作成して、対象の企業名を1行で記入
   - 例: `株式会社サンプル`

2. コマンドを実行（最短実行モード）
   ```bash
   cd marketing-agent
   pip install -r requirements.txt
   python src/run.py --quick --force
   ```
   - 直接指定したい場合は `--company "株式会社サンプル"` でも可

3. 生成物を確認
   - `marketing-agent/output/YYYYMMDD/` に分析テンプレートと動的ナレッジが生成されます
   - 例: `01_competitor-analysis.md`, `02_seo-analysis.md`, `knowledge/company-info.md`

補足:
- `--quick` は企業名以外の未設定（業界・地域など）を警告に緩和して実行します
- 競合URLが未設定の場合、競合サイト収集はスキップされます（警告のみ）

### 使い方（従来）
```bash
# 設定の検証（必須項目のチェック）
python src/workflows/config_loader.py

# プロジェクト作成（どちらでも可）
python src/workflows/setup-project.py
# または
python src/workflows/generic-setup-project.py
```
Cursor で `docs/prompts/quick-start.md` を実行すると、戦略とLP作成の手順をガイドします。

### ディレクトリ構成（シンプル）
```
marketing-agent/
├── input/                   # 入力（company-name.txt / project-config.yaml）
├── src/                     # 実行（run.py）
├── output/                  # 出力（YYYYMMDD 単位）
└── docs/                    # ユーザードキュメント
```

### トラブルシューティング（簡易）
- 設定が読み込めない: `python src/workflows/config_loader.py` を実行して必須項目（company.name, industry, location）を確認
- プロジェクトが生成されない: `output/` の作成権限を確認し、`python src/workflows/setup-project.py` を再実行
- SerpAPI を使う場合: Windows では `setx SERPAPI_KEY your_api_key` を設定

 

---
最終更新: 2025-01-27 / バージョン: v3.0