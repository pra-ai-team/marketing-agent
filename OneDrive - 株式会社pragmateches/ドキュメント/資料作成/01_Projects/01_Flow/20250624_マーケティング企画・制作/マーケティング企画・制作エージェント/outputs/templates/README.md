# テンプレートファイル使用方法

このディレクトリには、和光葬儀社マーケティング企画プロジェクトのテンプレートファイルが格納されています。

## テンプレートファイル一覧

1. **01_competitor-analysis.md** - 競合分析レポートテンプレート
2. **02_seo-analysis.md** - SEO分析・改善提案テンプレート
3. **03_marketing-strategy.md** - マーケティング戦略立案テンプレート
4. **04_lp-requirements.md** - LP要件定義テンプレート
5. **05_lp-completion-report.md** - LP完成レポートテンプレート

## 🔄 TODOマーカーの仕組み

### 新形式（推奨）: HTMLコメント形式
```markdown
<!-- TODO_EXECUTION_DATE -->
実行日時を記載
<!-- /TODO_EXECUTION_DATE -->
```

### 旧形式（互換性維持）
```markdown
TODO: 実行日時を記載
```

## 🤖 AIエージェントによる自動更新

新しいHTMLコメント形式のTODOマーカーは、AIエージェントが自動的に検索・置換できるように設計されています：

1. **一意のID**: 各TODOマーカーは固有のIDを持ちます（例：`TODO_EXECUTION_DATE`、`TODO_COMPETITOR_LIST`）
2. **明確な境界**: 開始タグ `<!-- TODO_XXX -->` と終了タグ `<!-- /TODO_XXX -->` で明確に範囲を定義
3. **検索しやすさ**: 正規表現による確実な検索・置換が可能

### 主要なTODOマーカーID

| ファイル | TODOマーカーID | 説明 |
|---------|---------------|------|
| 全ファイル | `TODO_EXECUTION_DATE` | 実行日時 |
| 01_competitor-analysis.md | `TODO_EXECUTIVE_SUMMARY` | エグゼクティブサマリー |
| 01_competitor-analysis.md | `TODO_COMPETITOR_LIST` | 競合企業リスト |
| 02_seo-analysis.md | `TODO_CURRENT_STATUS` | 現状評価 |
| 02_seo-analysis.md | `TODO_PRIMARY_KEYWORDS` | プライマリキーワード |
| 03_marketing-strategy.md | `TODO_STRATEGY_OVERVIEW` | 戦略概要 |
| 04_lp-requirements.md | `TODO_LP_PURPOSE` | LP目的 |
| 05_lp-completion-report.md | `TODO_LP_OVERVIEW` | 完成したLP概要 |

## 🚀 プロジェクト開始方法

### 自動セットアップ（推奨）
```bash
# 今日の日付でプロジェクト作成
python workflows/setup-project.py

# 特定日付でプロジェクト作成
python workflows/setup-project.py --date 20250625
```

### 手動セットアップ
```bash
# 新しい日付ディレクトリを作成
mkdir outputs/YYYYMMDD

# テンプレートをコピー
cp outputs/templates/*.md outputs/YYYYMMDD/
```

## 📝 作業手順

1. **プロジェクトセットアップ**: 上記の方法でプロジェクトディレクトリを作成
2. **STEP1から開始**: `01_competitor-analysis.md` のTODOマーカーを実際の内容に置き換え
3. **順次作業**: 前のSTEPの結果を参照しながら次のSTEPを進める
4. **完了確認**: すべてのTODOマーカーが実際の内容に更新されていることを確認

## ✅ 品質保証

- テンプレートは実際のプロジェクトから抽出された実証済みの構造
- TODOマーカーは必要な情報を漏れなく収集できるよう設計
- AIエージェントと人間の両方が効率的に作業できる形式
- 継続的改善により常に最新のベストプラクティスを反映

## 🔧 テンプレート改善

テンプレートの改善提案や新しいTODOマーカーの追加要望がある場合は、プロジェクトチームまでお知らせください。

---
*最終更新: 2025年6月25日* 