# 🚀 汎用マーケティング企画・制作エージェント

> **どんな業界・企業にも対応可能**　AI駆動型マーケティング戦略立案・LP制作システム

## 📋 概要

業界を問わず、どんな企業でも活用できるマーケティング戦略の立案からランディングページ制作まで、一連のプロセスを自動化・効率化するCursor専用システムです。

### 🎯 対応可能な業界・企業
- **どんな業界でも対応**: 美容・IT・飲食・製造・サービス業など
- **企業規模問わず**: スタートアップから大企業まで
- **地域限定なし**: 全国・海外でも対応
- **サービス形態自由**: BtoB・BtoC・オンライン・オフライン

### ⚡ 5分でスタート

```bash
# 1. 設定ファイルの準備
copy config/project-config.yaml.template config/project-config.yaml
# 企業・業界情報を記入

# 2. プロジェクト作成
python workflows/generic-setup-project.py

# 3. Cursorで実行
# @prompts/generic-quick-start.md をコピーして実行
```

### 🎯 最終成果物

- ✅ **競合分析レポート** - 任意業界の詳細な競合状況分析
- ✅ **SEO最適化戦略** - 地域・業界特化キーワード選定
- ✅ **マーケティング戦略** - 企業固有の戦略・ペルソナ・KPI設定  
- ✅ **LP要件定義書** - 実装可能な詳細仕様
- ✅ **高品質LP** - 即座に公開可能なHTML/CSS/JS

## 📁 プロジェクト構成

```
汎用マーケティング企画・制作エージェント/
├── 📋 config/                    # 設定ファイル
│   └── project-config.yaml       # ⭐ 企業・業界情報設定
├── 📋 prompts/                   # 汎用プロンプト
│   ├── generic-quick-start.md    # ⭐ クイックスタート
│   ├── generic-competitor-analysis.md
│   ├── generic-seo-analysis.md
│   └── generic-lp-development.md
├── 📚 knowledge/                 # 動的知識ベース
│   └── company-info.md           # 設定から自動生成
├── ⚙️ workflows/                 # 自動化ツール
│   ├── config_loader.py          # ⭐ 設定ファイル読み込み
│   ├── generic-setup-project.py  # プロジェクト自動セットアップ
│   └── generic-seo-analyzer.py   # 汎用SEO分析ツール
├── 📂 templates/                 # 汎用テンプレート
│   └── generic/                  # 業界非依存テンプレート
└── 📂 outputs/                   # 成果物格納
    └── YYYYMMDD/                 # 日付別プロジェクト
```

## 🚀 使用方法

### STEP 1: 設定ファイルの準備

1. **設定ファイルをコピー**:
```bash
copy config\project-config.yaml.template config\project-config.yaml
```

2. **企業・業界情報を記入**:
```yaml
# 基本企業情報
company:
  name: "あなたの企業名"
  industry: "あなたの業界"
  location: "営業地域"
  key_features:
    - "企業の特徴1"
    - "企業の特徴2"

# 競合企業情報
competitors:
  target_companies:
    - name: "競合企業A"
      website: "https://competitor-a.com"
    - name: "競合企業B"
      website: "https://competitor-b.com"

# SEO設定
seo:
  primary_keywords:
    - "メインキーワード1"
    - "メインキーワード2"
```

### STEP 2: プロジェクト作成

```bash
# 設定確認
python workflows/config_loader.py

# プロジェクト作成
python workflows/generic-setup-project.py
```

### STEP 3: マーケティング戦略・LP制作

```bash
# Cursorで以下を実行
@prompts/generic-quick-start.md
```

## 🎛️ システムの特徴

### ✨ 汎用性・柔軟性
- **業界フリー**: 設定ファイルで任意の業界に対応
- **企業規模フリー**: スタートアップから大企業まで
- **地域フリー**: 全国・海外対応
- **カスタマイズ可能**: 企業固有の要件に対応

### 🔧 自動化・効率化
- **設定ファイル連携**: 企業情報を一元管理
- **動的知識ベース**: 設定から自動生成
- **テンプレート自動更新**: 企業名・業界名を自動置換
- **品質保証**: TODOマーカーシステム

### 📊 実用性・品質
- **即座に使用可能**: 実際のプロジェクトに即適用
- **具体的な提案**: 実装可能な推奨事項
- **一貫性確保**: 全STEPで設定情報を参照
- **品質チェック**: 自動検証システム

## ⚙️ 技術環境

### 必要ツール
```bash
# Python環境（推奨: 3.8+）
pip install pyyaml requests python-dotenv

# SerpAPI設定（SEO分析用・オプション）
setx SERPAPI_KEY "your_api_key_here"
```

### 対応環境
- **OS**: Windows 10/11 (PowerShell)
- **エディタ**: Cursor（必須）
- **Python**: 3.8+ 
- **設定**: YAML形式
- **API**: SerpAPI（SEO分析用・オプション）

## 🎯 活用例

### 美容業界の場合
```yaml
company:
  name: "エステサロン美麗"
  industry: "美容業界"
  location: "東京都新宿区"
  key_features:
    - "完全個室対応"
    - "最新美容機器導入"
    - "経験豊富なエステティシャン"

competitors:
  target_companies:
    - name: "TBC"
      website: "https://www.tbc.co.jp"
    - name: "エステティックサロン"
      website: "https://www.esthe.co.jp"
```

### IT業界の場合
```yaml
company:
  name: "テックソリューション株式会社"
  industry: "IT業界"
  location: "全国（オンライン対応）"
  key_features:
    - "AI・機械学習特化"
    - "24時間サポート"
    - "業界最高水準のセキュリティ"

competitors:
  target_companies:
    - name: "アマゾン ウェブ サービス"
      website: "https://aws.amazon.com"
    - name: "Google Cloud"
      website: "https://cloud.google.com"
```

### 飲食業界の場合
```yaml
company:
  name: "イタリアンレストラン ベラヴィスタ"
  industry: "飲食業界"
  location: "大阪市北区"
  key_features:
    - "本格イタリアン"
    - "イタリア人シェフ"
    - "厳選素材使用"

competitors:
  target_companies:
    - name: "サイゼリヤ"
      website: "https://www.saizeriya.co.jp"
    - name: "カプリチョーザ"
      website: "https://www.capricciosa.com"
```

## 🔧 高度な設定

### 詳細な業界分析
```yaml
industry:
  characteristics:
    - "業界の特徴1"
    - "業界の特徴2"
  customer_behavior:
    - "顧客行動パターン1"
    - "顧客行動パターン2"
  challenges:
    - "業界の課題1"
    - "業界の課題2"
```

### SEO最適化設定
```yaml
seo:
  informational:    # 情報収集型
    - "○○とは"
    - "○○の選び方"
  navigational:     # 特定サイト検索型
    - "企業名"
    - "企業名 評判"
  transactional:    # 購買型
    - "○○ 申し込み"
    - "○○ 予約"
```

### ターゲット設定
```yaml
target_customers:
  primary:
    name: "メインターゲット"
    age: "30-50代"
    situation: "サービスを必要としている状況"
    needs: "高品質なサービスを求めている"
  secondary:
    name: "サブターゲット"
    age: "20-30代"
    situation: "価格を重視しながらサービスを検討"
    needs: "コストパフォーマンスの良いサービス"
```

## 🎯 活用のコツ

### 業界研究を深める
- 業界の市場規模・成長率を調査
- 顧客の行動パターンを分析
- 法規制・コンプライアンス要件を確認

### 競合分析を徹底
- 直接競合だけでなく間接競合も分析
- 価格・サービス・品質を多角的に比較
- デジタル対応力・SEO対策を詳細調査

### SEO戦略を戦略的に
- 地域性を活かしたキーワード選定
- 検索意図に応じたコンテンツ設計
- 競合の隙間を狙った差別化

### LP設計を効果的に
- ターゲットに響くキャッチコピー
- 競合優位性を明確に表現
- 行動喚起を戦略的に配置

## 📊 成功指標

### プロジェクト完了の目安
- [ ] 設定ファイルが正しく記入されている
- [ ] 全5つのSTEPファイルが作成済み
- [ ] TODOマーカーが0個（完全に更新済み）
- [ ] LPがブラウザで正常表示
- [ ] 業界特化の分析・戦略が含まれている

### 品質チェックリスト  
- [ ] 競合優位性が明確に表現されている
- [ ] ターゲットキーワードが適切に配置
- [ ] 業界特性に応じた分析が実施されている
- [ ] 実装可能な具体的推奨事項が含まれている
- [ ] レスポンシブデザインが機能
- [ ] ページ表示速度が3秒以内

### 成功のポイント

1. **設定ファイルを充実させる**
   - 企業の特徴・強みを具体的に記載
   - 業界特性を詳細に分析
   - 競合企業を幅広く設定

2. **キーワード選定を戦略的に**
   - 地域×サービス の組み合わせ
   - 検索意図別のキーワード設定
   - 競合が狙っていない隙間キーワード

3. **ターゲット設定を具体的に**
   - ペルソナを具体的に設定
   - 検索行動パターンを詳細に分析
   - 購買プロセスを考慮した設定

4. **品質管理を徹底**
   - 各STEPで前の結果を参照
   - TODOマーカーを完全に更新
   - 実装可能な具体的提案

## 🆘 トラブルシューティング

### よくある問題と解決方法

**❓ 設定ファイルが見つからない**
```bash
# 解決方法
ls config/
copy config\project-config.yaml.template config\project-config.yaml
```

**❓ 設定エラーが発生する**
```bash
# 解決方法
python workflows/config_loader.py
# 必須項目（company.name, industry, location）を確認・修正
```

**❓ 業界特化の分析が不十分**
```bash
# 解決方法
# config/project-config.yaml の以下を詳細に記入：
# - industry.characteristics (業界特徴)
# - industry.customer_behavior (顧客特性)
# - industry.challenges (業界課題)
```

**❓ 競合分析が物足りない**
```bash
# 解決方法
# config/project-config.yaml の以下を充実：
# - competitors.target_companies (3-7社)
# - competitors.analysis_points (分析観点)
```

**❓ プロジェクトが作成されない**
```bash
# 解決方法
# ディレクトリ権限を確認
mkdir outputs
python workflows/generic-setup-project.py
```

**❓ 業界特化の分析が不十分**
```bash
# 設定ファイルの industry.characteristics を詳細に記入
# 競合企業リストを業界に応じて更新
```

## 🔄 バージョン情報

- **現在バージョン**: v3.0 (2025年1月27日)
- **対応業界**: 全業界対応（汎用化完了）
- **対応企業**: 全企業対応（設定ファイル方式）

### 🔮 今後の予定
- [ ] 業界別テンプレートの追加
- [ ] 多言語対応
- [ ] API連携強化
- [ ] A/Bテスト機能の実装

## 📚 詳細ドキュメント

- **設定ファイル仕様**: [config/README.md](config/README.md)
- **プロンプト使用方法**: [prompts/README.md](prompts/README.md)
- **テンプレート仕様**: [templates/README.md](templates/README.md)
- **ワークフロー詳細**: [workflows/README.md](workflows/README.md)

---

## 🚀 今すぐ始める

### クイックスタート（3分）
```bash
# 1. 設定ファイル準備
copy config\project-config.yaml.template config\project-config.yaml
# 企業・業界情報を記入

# 2. プロジェクト作成
python workflows/generic-setup-project.py

# 3. Cursorで実行
# @prompts/generic-quick-start.md をコピーして実行
```

### 詳細セットアップ（5分）
```bash
# 1. 設定確認
python workflows/config_loader.py

# 2. 設定修正（必要に応じて）
# config/project-config.yaml を編集

# 3. プロジェクト作成
python workflows/generic-setup-project.py --date 20250127

# 4. 段階的実行
# @workflows/main.md を参照しながら STEP1-5 を実行
```

**🎯 目標**: あなたの企業が即座に使用可能な、高品質なマーケティング戦略とランディングページの提供

---
*最終更新: 2025年1月27日* 