# 汎用マーケティングツール - クイックスタートプロンプト

## 実行前の準備（最短）

1. 企業名を `input/company-name.txt` に1行で記入（例: 株式会社サンプル）
2. 以下を実行:
```bash
python workflows/setup-project.py --quick --force
```

従来フローを使いたい場合は次節を参照。

## 実行前の準備（従来）

**必須**: 以下の手順を実行して設定を確認してください：

1. **設定確認**:
```bash
python workflows/config_loader.py
```

2. **設定の問題がある場合**:
   - `input/project-config.yaml` を編集して企業・業界情報を記入
   - 再度設定確認を実行

3. **プロジェクト作成**:
```bash
python workflows/setup-project.py
```

## 実行プロンプト

```
@workflows/main.md を参照して、設定ファイルから読み込んだ企業情報に基づいて、マーケティング戦略とLP制作を実行してください。

## 実行手順

1. **設定情報の読み込み**: 
   - `python workflows/config_loader.py` を実行して設定情報を確認
   - 設定に問題がある場合は修正してください

2. **プロジェクト準備**: 
   - 本日の日付でプロジェクトディレクトリを作成
   - 汎用テンプレートを適用

3. **STEP1 - 競合分析**: 
   - @prompts/generic-competitor-analysis.md を参照
   - 設定ファイルの競合企業リストを分析
   - 業界特性に応じた分析観点を追加

4. **STEP2 - SEO・キーワード分析**: 
   - @prompts/generic-seo-analysis.md を参照
   - 設定ファイルのキーワード設定を活用
   - ターゲット地域・業界に特化したキーワード選定

5. **STEP3 - マーケティング戦略立案**: 
   - @prompts/generic-marketing-strategy.md を参照
   - STEP1-2の結果を統合
   - 設定ファイルのマーケティング目標を反映

6. **STEP4 - LP要件定義**: 
   - @prompts/generic-lp-requirements.md を参照
   - 設定ファイルのLP設定を反映
   - 全分析結果を統合した要件定義

7. **STEP5 - LP制作実装**: 
   - @prompts/generic-lp-development.md を参照
   - 実装可能な高品質なLP制作
   - 設定ファイルのデザイン傾向を反映

## 重要な注意点

1. **設定ファイル依存**: 
   - 各STEPで必ず設定ファイルの情報を参照してください
   - 企業名・業界・地域情報を動的に取得してください

2. **業界対応**: 
   - 設定された業界に応じた分析観点を追加してください
   - 業界特有の課題・機会を考慮してください

3. **TODOマーカー更新**: 
   - すべてのTODOマーカーを実際の内容に更新してください
   - 前のSTEPの結果を次のSTEPで必ず参照してください

4. **品質保証**: 
   - 最終的に公開可能な高品質なLPまで制作してください
   - 実装可能な具体的な推奨事項を提案してください

## 設定ファイルの活用方法

- **企業情報**: `config.get_company_info()`
- **業界情報**: `config.get_industry_info()`
- **競合情報**: `config.get_competitors_info()`
- **SEO設定**: `config.get_seo_config()`
- **ターゲット顧客**: `config.get_target_customers()`
- **マーケティング目標**: `config.get_marketing_goals()`
- **LP設定**: `config.get_landing_page_config()`

各STEPで上記の情報を適切に活用してください。
```

## 期待する成果物

### 必須成果物
- [ ] `01_competitor-analysis.md` - 業界特化の詳細競合分析
- [ ] `02_seo-analysis.md` - ターゲット地域・業界のSEO戦略
- [ ] `03_marketing-strategy.md` - 企業固有のマーケティング戦略
- [ ] `04_lp-requirements.md` - 実装可能なLP要件定義
- [ ] `05_lp-completion-report.md` - LP完成レポート
- [ ] `lp-files/` - 即座に公開可能なLP（HTML/CSS/JS）

### 品質基準
- 設定ファイルの企業・業界情報が正確に反映されている
- すべてのTODOマーカーが実際の内容に更新済み
- 各STEPが前のSTEPの結果を適切に参照している
- 業界特性に応じた分析・戦略が含まれている
- LPが即座に使用可能な品質で制作されている
- 実装可能な具体的な推奨事項が含まれている

## 進捗確認コマンド

```bash
# 進捗確認
python workflows/check-progress.py

# TODOマーカー残存確認
findstr /n "TODO" output\YYYYMMDD\*.md

# 設定情報確認
python workflows/config_loader.py
```

## 成功のポイント

1. **設定ファイル活用**: 汎用的な設定を活用して企業・業界に特化した分析を実行
2. **具体性**: 抽象的でなく、具体的な数値・データを含める
3. **一貫性**: 全STEPを通じて一貫した戦略を維持
4. **実用性**: 実際に使用可能な成果物を作成
5. **品質**: 妥協せず、最高品質を追求
6. **業界適応**: 設定された業界に適した分析・戦略を実行

## トラブルシューティング

**設定ファイルが見つからない場合**:
```bash
# 設定ファイルテンプレートを作成
mkdir input
cp input/project-config.yaml.template input/project-config.yaml
# 企業・業界情報を記入してください
```

**設定情報が不完全な場合**:
- `input/project-config.yaml`を編集
- 必須項目をすべて記入
- `python workflows/config_loader.py`で確認

**プロジェクトが作成されない場合**:
```bash
# 手動でディレクトリ作成
mkdir output
python workflows/setup-project.py
```

---

**最終目標**: 設定ファイルで指定された企業が即座に使用できる、高品質なマーケティング戦略とランディングページの提供

**実行開始**: 上記の手順に従って、設定ファイルベースのマーケティング戦略立案・LP制作を開始してください。