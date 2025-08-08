# テンプレート使用方法（汎用）

このディレクトリには業界非依存の標準テンプレートを配置します。

- 正式パス: `src/templates/generic/`
- 自動セットアップはこのパス（または後方互換の `templates/generic/`）を使用します

テンプレート一覧（generic）
- `01_competitor-analysis.md`
- `02_seo-analysis.md`
- `03_marketing-strategy.md`
- `04_lp-requirements.md`
- `05_lp-completion-report.md`

手動コピー例（PowerShell）
- 今日の日付で作業フォルダを作成: `New-Item -ItemType Directory -Path output/$(Get-Date -Format yyyyMMdd) -Force`
- テンプレートをコピー: `Copy-Item src/templates/generic/*.md output/YYYYMMDD/ -Force`

注意
- `output/templates/` は存在しません。テンプレートは `src/templates/generic/` を使用します（後方互換で `templates/generic/` も参照）。
 
最短実行
- `input/company-name.txt` に企業名を1行で保存
- `python workflows/setup-project.py --quick --force`