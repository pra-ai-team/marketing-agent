# 🚀 マーケティング企画・制作エージェント - 実行ガイド

## 📋 プロジェクト概要

**ミッション**: 和光葬儀社のマーケティング戦略立案からLP制作まで、一連の業務を自動化・効率化する

### 🎯 最終成果物
- ✅ 競合分析レポート
- ✅ SEO最適化戦略
- ✅ 包括的マーケティング戦略
- ✅ LP要件定義書
- ✅ 高品質なランディングページ（HTML/CSS/JS）

## 🔄 実行ワークフロー

### STEP 0: プロジェクト準備
```bash
# 自動セットアップ（推奨）
python workflows/setup-project.py

# 手動セットアップ
mkdir outputs/$(date +%Y%m%d)
cp outputs/templates/*.md outputs/$(date +%Y%m%d)/
```

### STEP 1: 競合分析 📊
**🎯 目標**: 葬儀業界の競合状況を把握し、和光葬儀社のポジショニングを明確化

**📁 入力**:
- `@knowledge/funeral-industry.md`
- `@knowledge/wakousougisya-company-info.md`

**📄 出力**: `01_competitor-analysis.md`

**✅ 完了条件**:
- [ ] 主要競合5-7社の詳細分析完了
- [ ] 和光葬儀社の競合優位性特定
- [ ] 市場ポジショニング図作成

### STEP 2: SEO・キーワード分析 🔍
**🎯 目標**: 検索エンジン最適化のための戦略的キーワード選定

**📁 入力**:
- `@knowledge/funeral-seo-keywords.md`
- STEP1の競合分析結果

**🤖 自動化ツール**: `workflows/seo-keyword-analyzer.py`

**📄 出力**: `02_seo-analysis.md` + JSONデータ

**✅ 完了条件**:
- [ ] ターゲットキーワード30個以上選定
- [ ] 競合SEO戦略分析完了
- [ ] キーワード難易度評価完了

### STEP 3: マーケティング戦略 📈
**🎯 目標**: 包括的なマーケティング戦略の策定

**📁 入力**:
- STEP1: 競合分析結果
- STEP2: SEO分析結果

**📄 出力**: `03_marketing-strategy.md`

**✅ 完了条件**:
- [ ] ターゲット顧客ペルソナ定義
- [ ] マーケティングチャネル戦略
- [ ] 具体的KPI設定

### STEP 4: LP要件定義 📝
**🎯 目標**: 実装可能なLP要件の詳細定義

**📁 入力**:
- STEP1-3の全分析結果

**📄 出力**: `04_lp-requirements.md`

**✅ 完了条件**:
- [ ] ワイヤーフレーム設計
- [ ] 技術仕様書作成
- [ ] コンテンツ設計完了

### STEP 5: LP制作実装 🎨
**🎯 目標**: 高品質なランディングページの制作

**📁 入力**:
- STEP4の要件定義

**📄 出力**: 
- `05_lp-completion-report.md`
- `lp-files/` ディレクトリ（HTML/CSS/JS）

**✅ 完了条件**:
- [ ] レスポンシブデザイン実装
- [ ] SEO最適化実装
- [ ] 動作テスト完了

## 🎛️ 品質管理システム

### TODOマーカー管理
```html
<!-- TODO_SECTION_NAME -->
置換対象のコンテンツ
<!-- /TODO_SECTION_NAME -->
```

### 進捗チェック
```bash
# TODOマーカー残存確認
findstr /n "TODO" outputs\YYYYMMDD\*.md

# 完了率確認
python workflows/check-progress.py
```

### 品質基準
- **🎯 完全性**: 全TODOマーカーが実際の内容に更新済み
- **🔗 一貫性**: 各STEPの結果が次STEPで適切に参照
- **⚡ 実用性**: 即座に使用可能な成果物品質
- **📊 測定可能**: 明確なKPIと成果指標

## 🛠️ 技術環境

### 必要なツール
```bash
# Python環境
pip install -r workflows/requirements.txt

# SerpAPI設定（SEO分析用）
setx SERPAPI_KEY "your_api_key_here"
```

### ディレクトリ構造
```
outputs/YYYYMMDD/
├── 01_competitor-analysis.md      # 競合分析
├── 02_seo-analysis.md             # SEO分析  
├── 03_marketing-strategy.md       # 戦略立案
├── 04_lp-requirements.md          # LP要件
├── 05_lp-completion-report.md     # 完了レポート
├── seo-data-YYYYMMDD.json         # SEOデータ
└── lp-files/                      # LP成果物
    ├── index.html
    ├── style.css
    ├── script.js
    └── README.md
```

## 🚀 クイックスタート

### 1回のコマンドで開始
```bash
# プロジェクト作成 → 初期プロンプト実行
python workflows/setup-project.py && echo "和光葬儀社のマーケティング戦略とLP制作を実行してください"
```

### プロンプト例
```
@workflows/main.md を参照して、和光葬儀社のマーケティング戦略とLP制作を実行してください。
STEP1の競合分析から順次進めて、最終的に公開可能なLPまで制作してください。
```

## 📊 成功指標

### プロジェクト完了条件
- [ ] 全5つのSTEPが完了
- [ ] TODOマーカーが0個
- [ ] LPが正常に動作
- [ ] SEO最適化スコア80%以上

### 品質チェックリスト
- [ ] 競合優位性が明確に表現されている
- [ ] ターゲットキーワードが適切に配置
- [ ] レスポンシブデザインが機能
- [ ] ページ表示速度が3秒以内

---

**💡 プロンプト実行時のコツ**
1. 各STEPで前の結果を必ず参照する
2. 具体的な数値・データを含める  
3. TODOマーカーを確実に更新する
4. 最終確認で品質チェックを実行

**🎯 最終目標**: 和光葬儀社が即座に使用可能な、高品質なマーケティング戦略とLPの提供
