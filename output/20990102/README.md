# サンプル株式会社 マーケティングプロジェクト - 20990102

## プロジェクト情報
- **開始日**: 2025年08月08日 10:01:07
- **対象企業**: サンプル株式会社
- **業界**: IT業界
- **プロジェクトディレクトリ**: `output/20990102/`

## 作業ファイル
1. `01_competitor-analysis.md` - 競合分析レポート
2. `02_seo-analysis.md` - SEO分析・改善提案
3. `03_marketing-strategy.md` - マーケティング戦略立案
4. `04_lp-requirements.md` - LP要件定義
5. `05_lp-completion-report.md` - LP完成レポート

## 動的生成ファイル
- `knowledge/company-info.md` - 設定ファイルから生成された企業・業界情報
- `project-summary.md` - プロジェクトサマリー

## 作業手順
1. `python workflows/config_loader.py` で設定を確認
2. 各ファイルの `<!-- TODO_XXX -->` マーカーを探す
3. マーカーで囲まれた部分を実際の内容に置き換える
4. 前のSTEPの結果を次のSTEPで参照する
5. 最終的にすべてのTODOマーカーを実際の内容に更新する

## 設定ファイル活用
- **企業情報**: `input/project-config.yaml`の company セクション
- **業界情報**: `input/project-config.yaml`の industry セクション
- **競合情報**: `input/project-config.yaml`の competitors セクション
- **SEO設定**: `input/project-config.yaml`の seo セクション

## 注意事項
- 設定ファイルの情報が各テンプレートに反映されています
- 業界に応じた分析観点を追加してください
- 実装可能な具体的な推奨事項を含めてください
- TODOマーカーは `<!-- TODO_XXX -->` と `<!-- /TODO_XXX -->` で囲まれています

## 品質チェック
- [ ] 設定ファイルの企業・業界情報が正確に反映されている
- [ ] すべてのTODOマーカーが実際の内容に更新されている
- [ ] 業界特性に応じた分析・戦略が含まれている
- [ ] 実装可能な具体的な推奨事項が含まれている

---
*このファイルは汎用マーケティングツールによって自動生成されました（2025年08月08日 10:01:07）*
